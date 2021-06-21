import unittest
from unittest import mock
from huey import RedisHuey, MemoryHuey
from django_huey.exceptions import ConfigurationError

from django_huey.config import DjangoHueySettingsReader

class DjangoHueyTests(unittest.TestCase):
    def test_djangohuey_config_with_no_settings(self):

        with self.assertRaises(ConfigurationError) as cm:
            config = DjangoHueySettingsReader(None)

        self.assertEqual('Error: DJANGO_HUEY must be a dictionary', str(cm.exception))


    def test_djangohuey_configure_does_not_raise_error_when_both_settings_are_defined(self):
        DJANGO_HUEY = {
            'queues': {
                'queuename': {
                    'name': 'test',
                    'immediate': True,
                }
            }
        }
        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()

    def test_djangohuey_get_queue_when_queue_is_none(self):
        DJANGO_HUEY = {
            'queues': {
                'queuename': {
                    'name': 'test',
                    'immediate': True,
                }
            }
        }
        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()

        with self.assertRaises(ConfigurationError) as cm:
            config.get_queue(None)

        self.assertEqual("""
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
""", str(cm.exception))

    def test_djangohuey_get_queue_when_queue_is_none_and_default_queue_is_defined(self):
        DJANGO_HUEY = {
            'default': 'queuename',
            'queues': {
                'queuename': {
                    'name': 'queue-default',
                    'immediate': True,
                }
            }
        }
        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()

        queue = config.get_queue(None)

        self.assertEqual(queue.name, 'queue-default')

    def test_djangohuey_invalid_default_queue(self):
        DJANGO_HUEY = {
            'default': 'invalid-queue',
            'queues': {
                'queuename': {
                    'name': 'queue-default',
                    'immediate': True,
                }
            }
        }
        with self.assertRaises(ConfigurationError) as cm:
            config = DjangoHueySettingsReader(DJANGO_HUEY)

        self.assertEqual("Queue defined as default: invalid-queue, is not configured in DJANGO_HUEY.", str(cm.exception))

    def test_djangohuey_configure_when_django_huey_setting_is_defined(self, *args):
        DJANGO_HUEY = {
            'queues': {
                'first': {
                    'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
                    'name': 'testname',  # Use db name for huey.
                },
                'mails': {
                    'huey_class': 'huey.MemoryHuey',  # Huey implementation to use.
                    'name': 'testnamememory',  # Use db name for huey.
                }
            }
        }

        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()

        self.assertTrue(isinstance(config.get_queue('first'), RedisHuey))
        self.assertEqual(config.get_queue('first').name, 'testname')
        self.assertTrue(isinstance(config.get_queue('mails'), MemoryHuey))
        self.assertEqual(config.get_queue('mails').name, 'testnamememory')

    def test_djangohuey_configure_when_django_huey_setting_is_an_object_raises_error(self, *args):
        DJANGO_HUEY = object()

        with self.assertRaises(ConfigurationError) as cm:
            config = DjangoHueySettingsReader(DJANGO_HUEY)

        self.assertEqual('Error: DJANGO_HUEY must be a dictionary', str(cm.exception))

    def test_djangohuey_if_name_is_not_defined_queue_name_is_default(self, *args):
        DJANGO_HUEY = {
            'queues': {
                'first': {
                    'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
                },
                'mails': {
                    'huey_class': 'huey.MemoryHuey',  # Huey implementation to use.
                }
            }
        }

        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()
        self.assertEqual(config.get_queue('first').name, 'first')

        self.assertEqual(config.get_queue('mails').name, 'mails')


    def test_djangohuey_with_backend_class(self, *args):
        DJANGO_HUEY = {
            'queues': {
                'first': {
                    'backend_class': 'huey.RedisHuey',
                }
            }
        }

        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()
        self.assertTrue(isinstance(config.get_queue('first'), RedisHuey))

    def test_djangohuey_invalid_backend_class(self, *args):
        DJANGO_HUEY = {
            'queues': {
                'first': {
                    'backend_class': 'huey.RedisHuey2',
                }
            }
        }

        with self.assertRaises(ConfigurationError) as cm:
            config = DjangoHueySettingsReader(DJANGO_HUEY)
            config.configure()

        self.assertEqual('Error: could not import Huey backend: huey.RedisHuey2', str(cm.exception))
