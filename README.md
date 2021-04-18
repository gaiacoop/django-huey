![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)

# django-huey

This package is an extension of [huey](https://github.com/coleifer/huey) contrib djhuey package that allows users to manage multiple queues.

## Compatible versions
| Package     | Version     |
| ----------- | ----------- |
| Django      | 3.1.x       |
| huey        | 2.3.x       |

## Installation

Using pip package manager run:
```
# pip install Django  if not installed
# pip install huey    if not installed
pip install django-huey
```

Note: use a virtualenv to isolate your dependencies.
Note 2: *django* and *huey* must be installed.

Then, in your **settings.py** file add django_huey to the INSTALLED_APPS:
```python
INSTALLED_APPS = [
	...
    'django_huey',
]
```

## Configuration
In **settings.py** you must add the HUEYS setting:
```python
HUEYS = {
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
```

## Usage
Now you will be able to run multiple queues using:
```
python manage.py run_djangohuey --queue first
python manage.py run_djangohuey --queue emails
```
Each queue must be run in a different terminal.

## Configuring tasks
You can use usual *huey* decorators to register tasks, but they must be imported from django_huey as shown below:

```python
from django_huey import db_task, task

@db_task(queue='first')
	# perform some db task

@task(queue='emails')
	# send some emails
```

All the args and kwargs defined in huey decorators should work in the same way, if not, let us know.
