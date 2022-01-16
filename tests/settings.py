DEBUG = True

DATABASES = {
    "default": {"NAME": "testdatabase", "ENGINE": "django.db.backends.sqlite3"}
}


SECRET_KEY = "django_tests_secret_key"
TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en-us"
ADMIN_MEDIA_PREFIX = "/static/admin/"
STATICFILES_DIRS = ()

MIDDLEWARE_CLASSES = []

INSTALLED_APPS = ["django_huey"]

DJANGO_HUEY = {
    "default": "multi-2",
    "queues": {
        "multi-1": {
            "huey_class": "huey.MemoryHuey",  # Huey implementation to use.
            "results": True,  # Store return values of tasks.
            "store_none": False,  # If a task returns None, do not save to results.
            "immediate": False,  # If DEBUG=True, run synchronously.
            "utc": True,  # Use UTC for all times internally.
            "blocking": True,  # Perform blocking pop rather than poll Redis.
            "consumer": {
                "workers": 1,
                "worker_type": "thread",
                "initial_delay": 0.1,  # Smallest polling interval, same as -d.
                "backoff": 1.15,  # Exponential backoff using this rate, -b.
                "max_delay": 10.0,  # Max possible polling interval, -m.
                "scheduler_interval": 60,  # Check schedule every second, -s.
                "periodic": True,  # Enable crontab feature.
                "check_worker_health": True,  # Enable worker health checks.
                "health_check_interval": 300,  # Check worker health every second.
            },
        },
        "multi-2": {
            "huey_class": "huey.MemoryHuey",  # Huey implementation to use.
            "results": True,  # Store return values of tasks.
            "store_none": False,  # If a task returns None, do not save to results.
            "immediate": False,  # If DEBUG=True, run synchronously.
            "utc": True,  # Use UTC for all times internally.
            "blocking": True,  # Perform blocking pop rather than poll Redis.
            "consumer": {
                "workers": 1,
                "worker_type": "thread",
                "initial_delay": 0.1,  # Smallest polling interval, same as -d.
                "backoff": 1.15,  # Exponential backoff using this rate, -b.
                "max_delay": 10.0,  # Max possible polling interval, -m.
                "scheduler_interval": 60,  # Check schedule every second, -s.
                "periodic": True,  # Enable crontab feature.
                "check_worker_health": True,  # Enable worker health checks.
                "health_check_interval": 300,  # Check worker health every second.
            },
        },
    },
}
HUEY = {
    "name": "test",
    "immediate": True,
}
