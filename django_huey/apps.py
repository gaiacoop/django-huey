from django.apps import AppConfig


class DjangoHueyConfig(AppConfig):
    name = "django_huey"

    def ready(self):
        try:
            monitor_installed = True
            from huey_monitor.tasks import startup_handler, store_signals
        except Exception:
            monitor_installed = False

        if monitor_installed:
            from django_huey.config import config
            from django_huey import signal, on_startup

            for queuename in config.hueys_setting.keys():
                signal(queue=queuename)(store_signals)
                on_startup(queue=queuename)(startup_handler)
