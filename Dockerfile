FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app

RUN apt-get update && apt-get --yes upgrade && apt-get --yes install build-essential libpq-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
