# DC-Monitor.web
## Link

[dcmonitor-dcm.herokuapp.com](dcmonitor-dcm.herokuapp.com)

## Clone
Clone the project
```
git clone https://github.com/erinallard/instagram_miner.git 
```
## Installation
Create and start a a virtual environment
```
virtualenv env --no-site-packages

source env/bin/activate 
```
Install the project dependencies:
```
pip install -r requirements.txt
```
Create Environment variables for :
```
SECRET_KEY="6a8cddef613e2ce8f14fa3d6e72b7c311adddf98a0f1252c"
DEBUG_VALUE="True" 
# to use it in settings file 
```
Environment variables Example in Settings :
```
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

Create a postgres DtataBase and add the credentials to settings.py 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Example_DB',
        'USER': 'Example',
        'PASSWORD': '****',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```
## Run 
Run makemigarations :
```
python manage.py makemigrations
```
Run migrate :
```
python manage.py migrate
```
Create Superadmin account :
```
python manage.py createsuperuser
```
To start the development server:
```
python manage.py runserver
```
Open lovalhost/admin panel and create Clint for your user. 
