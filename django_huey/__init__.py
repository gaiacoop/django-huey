from functools import wraps
from django.conf import settings
from django.db import close_old_connections

from django_huey.config import DjangoHueySettingsReader

DJANGO_HUEY = getattr(settings, "DJANGO_HUEY", None)

config = DjangoHueySettingsReader(DJANGO_HUEY)
config.configure()


def get_close_db_for_queue(queue):
    def close_db(fn):
        """Decorator to be used with tasks that may operate on the database."""

        @wraps(fn)
        def inner(*args, **kwargs):
            instance = get_queue(queue)
            if not instance.immediate:
                close_old_connections()
            try:
                return fn(*args, **kwargs)
            finally:
                if not instance.immediate:
                    close_old_connections()

        return inner

    return close_db


def get_queue(queue):
    return config.get_queue(queue)


def get_queue_name(queue):
    return config.get_queue_name(queue)


def task(*args, queue=None, **kwargs):
    return get_queue(queue).task(*args, **kwargs)


def context_task(*args, queue=None, **kwargs):
    return get_queue(queue).context_task(*args, **kwargs)


def periodic_task(*args, queue=None, **kwargs):
    return get_queue(queue).periodic_task(*args, **kwargs)


def lock_task(*args, queue=None, **kwargs):
    return get_queue(queue).lock_task(*args, **kwargs)


# Task management.


def enqueue(*args, queue=None, **kwargs):
    return get_queue(queue).enqueue(*args, **kwargs)


def restore(*args, queue=None, **kwargs):
    return get_queue(queue).restore(*args, **kwargs)


def restore_all(*args, queue=None, **kwargs):
    return get_queue(queue).restore_all(*args, **kwargs)


def restore_by_id(*args, queue=None, **kwargs):
    return get_queue(queue).restore_by_id(*args, **kwargs)


def revoke(*args, queue=None, **kwargs):
    return get_queue(queue).revoke(*args, **kwargs)


def revoke_all(*args, queue=None, **kwargs):
    return get_queue(queue).revoke_all(*args, **kwargs)


def revoke_by_id(*args, queue=None, **kwargs):
    return get_queue(queue).revoke_by_id(*args, **kwargs)


def is_revoked(*args, queue=None, **kwargs):
    return get_queue(queue).is_revoked(*args, **kwargs)


def result(*args, queue=None, **kwargs):
    return get_queue(queue).result(*args, **kwargs)


def scheduled(*args, queue=None, **kwargs):
    return get_queue(queue).scheduled(*args, **kwargs)


# Hooks.
def on_startup(*args, queue=None, **kwargs):
    return get_queue(queue).on_startup(*args, **kwargs)


def on_shutdown(*args, queue=None, **kwargs):
    return get_queue(queue).on_shutdown(*args, **kwargs)


def pre_execute(*args, queue=None, **kwargs):
    return get_queue(queue).pre_execute(*args, **kwargs)


def post_execute(*args, queue=None, **kwargs):
    return get_queue(queue).post_execute(*args, **kwargs)


def signal(*args, queue=None, **kwargs):
    return get_queue(queue).signal(*args, **kwargs)


def disconnect_signal(*args, queue=None, **kwargs):
    return get_queue(queue).disconnect_signal(*args, **kwargs)


def db_task(*args, **kwargs):
    queue = kwargs.get("queue")

    def decorator(fn):
        ret = task(*args, **kwargs)(get_close_db_for_queue(queue)(fn))
        ret.call_local = fn
        return ret

    return decorator


def db_periodic_task(*args, **kwargs):
    queue = kwargs.get("queue")

    def decorator(fn):
        ret = periodic_task(*args, **kwargs)(get_close_db_for_queue(queue)(fn))
        ret.call_local = fn
        return ret

    return decorator
