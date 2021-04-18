import sys

from importlib import import_module
from django.conf import settings
from huey.exceptions import ConfigurationError
from huey.contrib.djhuey import default_backend_path, get_backend


class DjangoHueySettingsReader:
    def __init__(self, hueys_setting):
        self.hueys_setting = hueys_setting
        self.hueys = {}

    def configure(self):
        if not isinstance(self.hueys_setting, dict):
            raise ConfigurationError('Error: HUEYS must be a dictionary')

        new_hueys = dict()
        for queue_name, config in self.hueys_setting.items():
            huey_config = config.copy()

            new_hueys[queue_name] = self._configure_instance(huey_config, queue_name)

        self.hueys_setting = new_hueys


    def default_queue(self, queue):
        if queue is None:
            raise ConfigurationError("""
If HUEYS is configured run_djangohuey must receive a --queue parameter
i.e.: 
python manage.py run_djangohuey --queue first
                """)
        return self.hueys_setting[queue]


    def _configure_instance(self, huey_config, default_queue_name):
        name = huey_config.pop('name', default_queue_name)
        if 'backend_class' in huey_config:
            huey_config['huey_class'] = huey_config.pop('backend_class')
        backend_path = huey_config.pop('huey_class', default_backend_path)
        conn_kwargs = huey_config.pop('connection', {})
        try:
            del huey_config['consumer']  # Don't need consumer opts here.
        except KeyError:
            pass
        if 'immediate' not in huey_config:
            huey_config['immediate'] = settings.DEBUG
        huey_config.update(conn_kwargs)

        try:
            backend_cls = get_backend(backend_path)
        except (ValueError, ImportError, AttributeError):
            raise ConfigurationError('Error: could not import Huey backend:\n%s'
                         % traceback.format_exc())

        return backend_cls(name, **huey_config)
