[![Python package](https://github.com/TheMerret/intensive-django/actions/workflows/python-package.yml/badge.svg)](https://github.com/TheMerret/intensive-django/actions/workflows/python-package.yml)

# Django Intensive

## Quick start

### Clone the repository:
```bash
git clone https://github.com/TheMerret/intensive-django.git
```

### Create a virtual environment:

Windows:
```bash
python -m venv venv
```
Mac, Linux:
```bash
python3 -m venv venv
```

### Activate the virtual environment:

Windows:
```bash
cd venv/Scripts/
```
```bash
.\activate
```
Mac, Linux:
```bash
source venv/bin/activate
```

### Install dependencies:

Windows:
```bash
pip install -r requirements.txt
```
Mac, Linux:
```bash
pip3 install -r requirements.txt
```

For development:

```
requirements-dev.txt
```

For testing:

```
requirements-test.txt
```

### Configure

You should use dotenv to configure settings. Example:

```
SECRET_KEY = VERYSECRETKEY
DEBUG = false
ALLOWED_HOSTS = 192.168.0.21,192.168.0.1
```

### Launch:

#### Django server:

Windows:
```bash
python manage.py runserver
```
Mac, Linux:
```bash
python3 manage.py runserver
```
## For developers

[Django](https://docs.djangoproject.com/en/3.2/) documentation

### Custom commands

### `initdata`

If you want to populate your fresh db with fixtures and superuser creditinals you can use

Windows:
```bash
python manage.py initdata
```
Mac, Linux:
```bash
python3 manage.py initdata
```

This command will check migrations and if there are pending ones you can apply them in place.

After that command will create superuser with creditinals defined in enviroment variables like

```
DJANGO_SUPERUSER_USERNAME = TheMerret
DJANGO_SUPERUSER_EMAIL = themerret@email.com
DJANGO_SUPERUSER_PASSWORD = superuserpassword
```

You could input all your creditinal from stdin if you haven't specified settings in enviroment variables. 

## Models' schemes

[Schemes](https://gist.github.com/TheMerret/9cb1a73c9639e0f737f273a390c88f88)
