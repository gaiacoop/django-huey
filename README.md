![Version](https://img.shields.io/badge/version-1.0.0-informational.svg)

# django-huey

This package is an extension of [huey](https://github.com/coleifer/huey) contrib djhuey package that allows users to manage multiple queues.

## Compatible versions
| Package     | Version     |
| ----------- | ----------- |
| Django      | 2.2         |
| Django      | 3.1         |
| Django      | 3.2         |
| huey        | 2.3         |

## Installation

Using pip package manager run:
```
pip install django-huey
```

Note: use a virtualenv to isolate your dependencies.

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


## Configuring tasks
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
