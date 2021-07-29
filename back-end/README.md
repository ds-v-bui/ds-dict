# dsvn_dictionary
- if not install lib mysql:
run command: 
1.pip install pymysql

- after open settings.py and change declaration of DATABASES:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
- install the django-cors-headers library:
1.pip install django-cors-headers

- authentication jwt in django:
1.pip install djangorestframework-simplejwt

- import or export file excel:
1. pip install django-import_export

- create superuser:
1.python manage.py createsuperuser

- Google API Speech-to-Text:
1.pip install SpeechRecognition
2.pip install pipwin
3.pipwin install pyaudio

- Google translate api:
1. pip install googletrans==3.1.0a0

- run command:
1.python manage.py makemigrations 
2.python manage.py migrate
