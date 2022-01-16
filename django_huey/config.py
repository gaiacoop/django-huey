from django.conf import settings
from django_huey.exceptions import ConfigurationError
from huey.contrib.djhuey import default_backend_path, get_backend


class DjangoHueySettingsReader:
    def __init__(self, hueys_setting):
        if not isinstance(hueys_setting, dict):
            raise ConfigurationError("Error: DJANGO_HUEY must be a dictionary")
        self.hueys_setting = hueys_setting.get("queues")
        self.default_queue = hueys_setting.get("default")

        if (
            self.default_queue is not None
            and self.default_queue not in self.hueys_setting
        ):
            raise ConfigurationError(
                f"Queue defined as default: {self.default_queue}, is not configured in DJANGO_HUEY."
            )
        self.hueys = {}

    def configure(self):
        new_hueys = dict()
        for queue_name, config in self.hueys_setting.items():
            huey_config = config.copy()

            new_hueys[queue_name] = self._configure_instance(huey_config, queue_name)

        self.hueys_setting = new_hueys

    def get_queue(self, queue):
        return self.hueys_setting[self.get_queue_name(queue)]

    def get_queue_name(self, queue_name):
        if queue_name is None:
            if self.default_queue is None:
                self._raise_queue_config_error()

            queue_name = self.default_queue
        return queue_name

    def _raise_queue_config_error(self):
        raise ConfigurationError(
            """
Command djangohuey must receive a --queue parameter or define a default queue in DJANGO_HUEY setting.
i.e.:
python manage.py djangohuey --queue first

or in settings file:

DJANGO_HUEY = {
    'default': 'your-default-queue-name',
    'queues': {
        #Your queues here
    }
}
"""
        )

    def _configure_instance(self, huey_config, default_queue_name):
        name = huey_config.pop("name", default_queue_name)
        if "backend_class" in huey_config:
            huey_config["huey_class"] = huey_config.pop("backend_class")
        backend_path = huey_config.pop("huey_class", default_backend_path)
        conn_kwargs = huey_config.pop("connection", {})
        try:
            del huey_config["consumer"]  # Don't need consumer opts here.
        except KeyError:
            pass
        if "immediate" not in huey_config:
            huey_config["immediate"] = settings.DEBUG
        huey_config.update(conn_kwargs)

        try:
            backend_cls = get_backend(backend_path)
        except (ValueError, ImportError, AttributeError):
            raise ConfigurationError(
                f"Error: could not import Huey backend: {backend_path}"
            )

        return backend_cls(name, **huey_config)
