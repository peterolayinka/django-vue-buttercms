# Description

Implementation of the use of ButterCMS with Django and Vue.js Integration.

## Installation

- Ensure you have python3 installed.
- RUN `python3 -m venv venv` to create a virtual environment
- RUN `source ./venv/bin/activate` to enable the virtual env
- RUN `pip install -r requirements.txt` to install required libraries.
- Make a copy of the `.env.sample` file
- Rename the file to `.env` and add the neccessary credentials.


## Launch APP

- RUN `python manage.py runserver` to start the app
- RUN `python manage.py collectstatic` to access static files when `DEBUG=False` (Note: this is important for the Vue.js app when `DEBUG=False`)
- The RUN the app again `python manage.py runserver`


## All Available Endpoint/URL

- http://localhost:8000 (Index Page)
- http://localhost:8000/blog/ (Blog Home Page)
- http://localhost:8000/blog/<slug> (Blog Post Detail Page)

## Test

- RUN `python manage.py test`

### Test Coverage

The Django app has about 99% test coverage

- RUN `coverage3 run manage.py test`
- RUN `coverage3 report`