"""
Django settings for RunPlayers project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#zu5%$)z(ya!-0mo_agc-@_gwiz4wtuk3j7e)htw89nuyjt2j1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'FutboolGruops',
    'social.apps.django_app.default',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
)
REST_FRAMEWORK = {
     # Use hyperlinked styles by default.
     # Only used if the `serializer_class` attribute is not set on a view.
     'DEFAULT_MODEL_SERIALIZER_CLASS':
         'rest_framework.serializers.HyperlinkedModelSerializer',

     # Use Django's standard `django.contrib.auth` permissions,
     # or allow read-only access for unauthenticated users.
     'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
     ],
     'DEFAULT_FILTER_BACKENDS': [
            'rest_framework.filters.DjangoFilterBackend',
        ]
}

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   #'social.backends.google.GoogleOAuth2',
   #'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
    )
SOCIAL_AUTH_FACEBOOK_KEY = '1693585214201836'
SOCIAL_AUTH_FACEBOOK_SECRET = '1e1f5c43f9c653a26c4ce2785865b2a0'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'publish_actions']

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
LOGIN_ERROR_URL = '/error'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/error'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/homes/0'

AUTH_USER_MODEL = 'FutboolGruops.User'

SOCIAL_AUTH_USER_MODEL = 'FutboolGruops.User'

CORS_ORIGIN_ALLOW_ALL = True

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'FutboolGruops.pipeline.get_profile_picture',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

ROOT_URLCONF = 'RunPlayers.urls'

WSGI_APPLICATION = 'RunPlayers.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': '',
        #'HOST': 'ec2-54-83-20-177.compute-1.amazonaws.com',
        #'USER': 'fikjmqsvcxsyze',
        #'PORT': '5432',
        #'PASSWORD': '',
    #}
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ar'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#AUTH_PROFILE_MODULE = 'futbolitoDomingero.Jugadores'
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]