# Automation Manual Documentation

* ## Local Deployment Using Docker

    1. Get a valid `.env` from your team lead and put inside the project directory and modify it with your preferred
       configurations.
    2. run `pip install pipenv`
    3. run `pipenv install -d`
    4. run `python manage.py migrate`
    5. run `python manage.py runserver

* ## Note

    * For development and maintenance please install git hooks using: `pre-commit install`
    * Swagger Address: `{BASE_URL}/api/schema/swagger-ui/`
    * add `Token` prefix before token for authentication E.g : `Token ec40c5c6278df6a90855934f8b287ed8b5c38ad3`
