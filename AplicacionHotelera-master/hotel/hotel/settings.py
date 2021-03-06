"""
Django settings for hotel project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm9#@w(e_l%y1$r(xxin2o17_=czb^98le!!!alt2f%^$lvl_$r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # app creadas
    'social_django',  # social
    'rest_framework',    
    'rest_framework.authtoken',
    'accesos.apps.AccesosConfig',
    'reservas.apps.ReservasConfig',
    'shopping_cart.apps.ShoppingCartConfig',
    'card.apps.CardConfig',
    'cardToken.apps.CardtokenConfig',
    'tour_package.apps.TourPackageConfig',
    'administracion.apps.AdministracionConfig',
    'noticias.apps.NoticiasConfig',
    'contact.apps.ContactConfig',
    'chat.apps.ChatConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'hotel/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'reservas.context_processors.add_variable_to_context',                
            ],
        },
    },
    
]


WSGI_APPLICATION = 'hotel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

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

# Autenticaciones
AUTHENTICATION_BACKENDS = [
    # 'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accesos.Usr'
SOCIAL_AUTH_USER_MODEL = 'accesos.Usr'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/accesos/login_social'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/accesos/registro_social'

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("FbKey","484372565697357")        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("FbSecret","e919caa80a98637c70827cb7fba27f2c") # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link'] # add this
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {       # add this
  'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [                 # add this
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]


# add this code
SOCIAL_AUTH_INSTAGRAM_KEY = '438ed7db10664d158692eab9b62cc343'         #Client ID
SOCIAL_AUTH_INSTAGRAM_SECRET = 'add65e6365bd4d3f90ad10e47db250e9'  #Client SECRET
SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = [               
    ('user', 'user'),
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='777067359855-950lfd7lr49033eorucjdp7iksrbtn8q'  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Vbao4N2CRw6DJSIlvn0QMzmJ' #Paste Secret Key

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#MEDIA_ROOT = os.path.join(BASE_DIR,'recursos/')
# MEDIA_ROOT = "C:/Users/gabpa/Documents/Proyecto Software/hotel emilio/AplicacionHotelera/recursos/"

MEDIA_URL = '/recursos/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'recursos/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "hotel/static"),
]

#Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hotelsalinas2020@gmail.com'
EMAIL_HOST_PASSWORD = 'hotel123salinas'