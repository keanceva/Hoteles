# AplicacionHotelera

Datos de la base:
/hotel/hotel/settings.py

...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "hotel",
        'USER': "postgres",
        'PASSWORD': "root",
        'HOST': "localhost",
        'PORT': "5432",
    }
}
...

Después de haberlo clonado
/hotel

Para compilar:
- python manage.py makemigrations tour_package
- python manage.py migrate tour_package
- python manage.py makemigrations accesos
- python manage.py migrate accesos
- python manage.py migrate sessions
- python manage.py migrate social_django
- python manage.py makemigrations reservas
- python manage.py migrate reservas
- python manage.py makemigrations shopping_cart
- python manage.py migrate shopping_cart
- python manage.py makemigrations noticias
- python manage.py migrate noticias
- python manage.py runserver

Si se ha hecho un pull, para que no exista conflicto con los migrate en la db se debe hacer:
- Eliminar en cada app, la carpeta __pycache__ que se encuentra en la carpeta migrations de cada app.
- Eliminar todos los archivos .py a excepción del __init__.py, que se encuentran en la carpeta migrations de cada app.
- Eliminar cada tabla de la base de datos, o eliminar directamente la base de datos completa.
- Repetir de nuevo los pasos para compilar.

Para llenar la db con data, utilizar el archivo db_data.sql que se encuentra en la carpeta db.
