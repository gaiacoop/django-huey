 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![Version](https://img.shields.io/badge/version-1.2.0-informational.svg)

# django-huey

***

This package is an extension of [huey](https://github.com/coleifer/huey) contrib djhuey package that allows users to manage multiple queues.

## Compatible versions
| Package     | Version     |
| ----------- | ----------- |
| Django      | 5.0         |
| Django      | 4.2         |
| Django      | 3.2         |
| huey        | 2.5         |
| huey        | 2.4         |

## Installation

Using pip package manager run:
```
pip install django-huey
```

Then, in your **settings.py** file add django_huey to the INSTALLED_APPS:
```python
INSTALLED_APPS = [
	...
    'django_huey',
]
```

## Configuration
In **settings.py** you must add the DJANGO_HUEY setting:
```python
DJANGO_HUEY = {
    'default': 'first', #this name must match with any of the queues defined below.
    'queues': {
        'first': {#this name will be used in decorators below
            'huey_class': 'huey.RedisHuey',  
            'name': 'first_tasks',  
            'consumer': {
                'workers': 2,
                'worker_type': 'thread',
            },
        },
        'emails': {#this name will be used in decorators below
            'huey_class': 'huey.RedisHuey',  
            'name': 'emails_tasks',  
            'consumer': {
                'workers': 5,
                'worker_type': 'thread',
            },
        }
    }
}
```

### Including queues from files
*new in 1.1.0*

You can also include a queue configuration from another file, located in one of your apps.
Use django_huey.utils.include to do so:

In **settings.py** you may have:
```python
DJANGO_HUEY = {
    'default': 'first', #this name must match with any of the queues defined below.
    'queues': {
        # Your current queues definitions
    }
}

# This is new
from django_huey.utils import include
DJANGO_HUEY["queues"].update(include("example_app.queues"))
```

And in your `example_app.queues`:
```python
queues = {
    "test": {
        "huey_class": "huey.MemoryHuey",
        "results": True,
        "store_none": False,
        "immediate": False,
        "utc": True,
        "blocking": True,
        "consumer": {
            "workers": 1,
            "worker_type": "thread",
            "initial_delay": 0.1,
            "backoff": 1.15,
            "max_delay": 10.0,
            "scheduler_interval": 60,
            "periodic": True,
            "check_worker_health": True,
            "health_check_interval": 300,
        },
    },
}
```
Note: in your queues file, you should declare a variable called `queues`, so they can be included. If the variable doesn't exist, an `AttributeError` will be raised.

### Usage
Now you will be able to run multiple queues using:
```
python manage.py djangohuey --queue first
python manage.py djangohuey --queue emails
```
Each queue must be run in a different terminal.

If you defined a default queue, you can just run:
```
python manage.py djangohuey
```
And the default queue will be used.


### Configuring tasks
You can use usual *huey* decorators to register tasks, but they must be imported from django_huey as shown below:

```python
from django_huey import db_task, task

@task() #Use the default queue 'first'
def some_func_that_uses_default_queue():
    # perform some db task
    pass

@db_task(queue='first')
def some_func():
    # perform some db task
    pass

@task(queue='emails')
def send_mails():
	# send some emails
    pass
```

All the args and kwargs defined in huey decorators should work in the same way, if not, let us know.

### Importing a huey instance
Sometimes you'll need to import a huey instance in order to do some advanced configuration, for example, when using huey pipelines.

You can do that by using the get_queue function from django_huey:
```python
from django_huey import get_queue

first_q = get_queue('first')

@first_q.task()
def some_func():
    pass
```

### Integration with huey monitor
You can use django-huey with [huey monitor](https://github.com/boxine/django-huey-monitor).
