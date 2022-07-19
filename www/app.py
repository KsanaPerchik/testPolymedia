import logging
import marshmallow as ma

from flask import Flask
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from .extensions import db, api  # @UnresolvedImport
from .models import Deck, Card

log = logging.getLogger(__name__)

DEFAULT_DECK = 'default'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['API_TITLE'] = 'TestAPI'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.1.0'
app.config['OPENAPI_URL_PREFIX'] = 'doc'
app.config['OPENAPI_REDOC_PATH'] = 'redoc'
app.config['OPENAPI_REDOC_URL'] = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
api.init_app(app)


def create_db():
    with app.app_context():
        db.create_all()


def create_deck(name=DEFAULT_DECK):
    """Instantiate default deck"""
    with app.app_context():
        if not get_deck():
            item = Deck(name=name)
            db.session.add(item)
            db.session.commit()


def get_deck(name=DEFAULT_DECK):
    return Deck.query.filter_by(name=name).one_or_none()  # @UndefinedVariable

create_db()
create_deck()


@app.route('/')
def greetings():
    return '<p>Привет! Твоя задача - написать автотесты к моему API (/api).</p>'


@app.route('/api')
def api_info():
    return {'version': app.config['API_VERSION']}


class DeckSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String(required=True)
    size = ma.fields.Int()


class DeckQueryArgsSchema(ma.Schema):
    name = ma.fields.String()


class CardSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    rank = ma.fields.String(required=True)
    suit = ma.fields.String(required=True)


class CardQueryArgsSchema(ma.Schema):
    rank = ma.fields.String()
    suit = ma.fields.String()

blp = Blueprint('casino', 'casino', url_prefix='/api', description="Let's have some fun!")


@blp.route('/decks')
class Decks(MethodView):
    @blp.arguments(DeckQueryArgsSchema, location='query')
    @blp.response(200, DeckSchema(many=True))
    def get(self, args):
        """List decks"""
        query = Deck.query  # @UndefinedVariable

        if 'name' in args:
            query = query.filter_by(name=args['name'])

        return query.all()


@blp.route('/decks/<int:deck_id>')
class DeckById(MethodView):
    @blp.response(200, DeckSchema)
    def get(self, deck_id):
        """Get deck by ID"""
        try:
            item = Deck.query.filter_by(id=deck_id).one()  # @UndefinedVariable
        except NoResultFound:
            abort(404)
        return item


@blp.route('/decks/<int:deck_id>/cards')
class Cards(MethodView):
    @blp.arguments(CardQueryArgsSchema, location='query')
    @blp.response(200, CardSchema(many=True))
    def get(self, *args, **kwargs):
        """List cards"""
        query = Card.query.filter_by(deck_id=kwargs['deck_id'])  # @UndefinedVariable

        if args:
            data = args[-1]
            query = query.filter_by(**data)

        return query.all()

    @blp.arguments(CardSchema)
    @blp.response(201, CardSchema)
    def post(self, *args, **kwargs):
        """Add a new card"""
        deck = get_deck()
        data = args[-1]
        item = Card(rank=data['rank'], suit=data['suit'], deck_id=kwargs['deck_id'])

        try:
            db.session.add(item)
            deck.cards.append(item)
            db.session.commit()
        except IntegrityError:
            abort(400)

        return item


@blp.route("/decks/<deck_id>/cards/<card_id>")
class CardById(MethodView):
    @blp.response(200, CardSchema)
    def get(self, deck_id, card_id):
        """Get card by ID"""
        try:
            item = Card.query.filter_by(deck_id=deck_id, id=card_id).one()  # @UndefinedVariable
        except NoResultFound:
            abort(404)
        return item

    @blp.response(204)
    def delete(self, deck_id, card_id):
        """Delete card"""
        try:
            item = Card.query.filter_by(deck_id=deck_id, id=card_id).one()  # @UndefinedVariable
            db.session.delete(item)
            db.session.commit()
        except NoResultFound:
            abort(404)

api.register_blueprint(blp)
