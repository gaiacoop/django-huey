DEBUG = True

DATABASES = {
    "default": {
        'NAME': 'testdatabase',
        "ENGINE": "django.db.backends.sqlite3"
    }
}


SECRET_KEY = "django_tests_secret_key"
TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en-us"
ADMIN_MEDIA_PREFIX = "/static/admin/"
STATICFILES_DIRS = ()

MIDDLEWARE_CLASSES = []

INSTALLED_APPS = [
    "django_huey"
]

DJANGO_HUEY = {
    'queues': {}
}
HUEY = {
    'name': 'test',
    'immediate': True,
}
