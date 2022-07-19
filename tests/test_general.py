import requests


def test_smoke():
    r = requests.get('http://0.0.0.0:5000/api')
    assert 200 == r.status_code
    assert r.json() == {"version": "v1"}
