### Веб-приложение с API
#### Развертывание
- установить docker (https://docs.docker.com/get-docker/)
- установить docker-compose (https://docs.docker.com/compose/install/)
- создать форк проекта `https://gitlab.com/ru-r5/testme` в своем аккаунте на `gitlab.com`
- клонировать локально репозиторий форка (например,`git clone git@gitlab.com:yourname/testme.git`)
- перейти в директорию склонированного репозитория
- запустить приложение (`docker compose up -d --build`)

#### Запуск
- запустить тесты (`docker exec -i testme-flask-api pytest`)
- открыть браузер (`http://0.0.0.0:5011`)

#### Задача
- добавить в директорию ./tests файл с несколькими простыми тестами, например:
  - получение карт по масти и номиналу
  - добавление карты в колоду
  - удаление карты из колоды
  - получение карты, отсутствующей в колоде
  - передача неизвестных атрибутов в запросе
- оформить результаты тестирования на свое усмотрение

#### Дополнительная информация
  - известные масти:
    - CLUB
    - DIAMOND
    - HEART
    - SPADE
  - известные номиналы
    - ACE
    - TWO
    - TREE
    - FOUR
    - FIVE
    - SIX
    - SEVEN
    - EIGHT
    - NINE
    - TEN
    - JACK
    - QUEEN
    - KING
  - описание API: `http://0.0.0.0:5011/doc/redoc`