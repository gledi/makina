Installation Instructions
=========================

Clone the repo

```
git clone https://github.com/gledi/makina.git
```

Enter repo and create virtual environment

```
cd makina
python -m venv --prompt=makina venv
. venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run migrations

```
python manage.py migrate vehicles
```

Run local development server

```
python manage.py runserver
```

Visit the following url on your browser: http://localhost:8000/

Deploy
======

