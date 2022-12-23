# ИС Автомастерская

## Стек: python3.9, Django, Postgres, DRF

---

Создание виртуального окружения и установка необходимых зависимостей: 
- poetry install

Запуск приложения:

- docker run --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:latest
- python manage.py migrate
- python manage.py runserver

Запуск тестов:

- poetry run pytest

---

### Структура проекта:

Проект состоит из 3х приложений:

- users — приложение для работы с пользователями;
- cars — приложение с автомобилями;
- orders — приложение для работы с заказами и реестрами. Здесь реализован основной функционал проекта.

#### Users:
Модель пользователя создана на основе AbstractUser. Реализованы методы:

- регистрация пользователя(для физических(клиент/работник) и юридических лиц);
- JWT-авторизация;
- получение данных пользователя;
- обновление данных пользователя;
- смена пароля;
- получение списка пользователей.

Реализованы permissions для пользователей(получение/редактирование/удаление информации только о себе) и работников(все методы)

#### Cars:
Модель автомобиля. Реализованы методы:

- добавление автомобиля в систему;
- получение данных об автомобиле;
- обновление данных об автомобиле;
- получение списка автомобилей;
- получение списка автомобилей пользователя.

Реализованы permissions для пользователей(получение списка только своих авто, создание авто) и работников(все методы)

#### Orders:
Модели:

- **SparePartRegister** - реестр запчастей;
- **Purchase** - закупка;
- **ServiceRegister** - реестр услуг;
- **Order** - заказ;
а также промежуточные модели для некоторых M2M отношений

Для каждой модели реализованы методы:
- добавление модели в систему;
- получение данных о модели;
- обновление данных о модели;
- получение списка моделей;

Для Orders также есть
- получение списка заказов пользователя.

Реализованы permissions для пользователей(получение списка только своих заказов) и работников(все методы)

Написаны тесты для методов *create*, *update*, *destroy*
