from importlib import import_module
from django_huey.exceptions import ConfigurationError
from django_huey import config


def include(path):
    if isinstance(path, str):
        try:
            queue_module = import_module(path)
        except ModuleNotFoundError:
            raise ConfigurationError(
                f"No module named '{path}'. Review included queues modules in DJANGO_HUEY."
            )
    queues = getattr(queue_module, "queues")
    config.include(queues)
    return queues
