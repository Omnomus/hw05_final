# Проект Yatube
Проект Yatube - это социальная сеть, она дает возможность пользователям создать учетную запись, постить записи (в том числе с картинками), подписываться на любимых авторов и комментировать посты других людей. Для записи можно выбрать одну из существующих групп, наиболее подходящую по тематике. 

Добавление новых групп осуществляется в админ панели. 

В проекте были реализованы пагинация, кэширование, написаны unittest. 

Следующие технологии были использованы при создании проекта:
- Python 3.8.2
- Django REST 2.2.6
- pytest
- Bootstrap
- Git
- SQLite3

Установка:
1. Клонируем репозиторий на локальную машину: $ git clone https://github.com/Omnomus/hw05_final
2. Создаем виртуальное окружение: $ python -m venv venv
3. Устанавливаем зависимости: $ pip install -r requirements.txt
4. Создание и применение миграций: $ python manage.py makemigrations и $ python manage.py migrate
5. Запускаем django сервер: $ python manage.py runserver


