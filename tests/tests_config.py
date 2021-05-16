import unittest
from huey import RedisHuey, MemoryHuey
from django_huey.exceptions import ConfigurationError

from django_huey.config import DjangoHueySettingsReader

class DjangoHueyTests(unittest.TestCase):
    def test_djangohuey_config_with_no_settings(self):
        config = DjangoHueySettingsReader(None)

        with self.assertRaises(ConfigurationError) as cm:
            config.configure()

        self.assertEqual('Error: DJANGO_HUEY must be a dictionary', str(cm.exception))


    def test_djangohuey_configure_does_not_raise_error_when_both_settings_are_defined(self):
        DJANGO_HUEY = {
            'queuename': {
                'name': 'test',
                'immediate': True,
            }
        }
        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()

    def test_djangohuey_default_queue_when_queue_is_none(self):
        DJANGO_HUEY = {
            'queuename': {
                'name': 'test',
                'immediate': True,
            }
        }
        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()

        with self.assertRaises(ConfigurationError) as cm:
            config.default_queue(None)

        self.assertEqual("""
Command djangohuey must receive a --queue parameter
i.e.: 
python manage.py djangohuey --queue first
                """, str(cm.exception))

    def test_djangohuey_configure_when_django_huey_setting_is_defined(self, *args):
        DJANGO_HUEY = {
            'first': {
                'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
                'name': 'testname',  # Use db name for huey.
            },
            'mails': {
                'huey_class': 'huey.MemoryHuey',  # Huey implementation to use.
                'name': 'testnamememory',  # Use db name for huey.
            }
        }

        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()

        self.assertTrue(isinstance(config.default_queue('first'), RedisHuey))
        self.assertEqual(config.default_queue('first').name, 'testname')
        self.assertTrue(isinstance(config.default_queue('mails'), MemoryHuey))
        self.assertEqual(config.default_queue('mails').name, 'testnamememory')

    def test_djangohuey_configure_when_django_huey_setting_is_an_object_raises_error(self, *args):
        DJANGO_HUEY = object()

        config = DjangoHueySettingsReader(DJANGO_HUEY)

        with self.assertRaises(ConfigurationError) as cm:
            config.configure()
        self.assertEqual('Error: DJANGO_HUEY must be a dictionary', str(cm.exception))

    def test_djangohuey_if_name_is_not_defined_queue_name_is_default(self, *args):
        DJANGO_HUEY = {
            'first': {
                'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
            },
            'mails': {
                'huey_class': 'huey.MemoryHuey',  # Huey implementation to use.
            }
        }

        config = DjangoHueySettingsReader(DJANGO_HUEY)

        config.configure()
        self.assertEqual(config.default_queue('first').name, 'first')

        self.assertEqual(config.default_queue('mails').name, 'mails')


if __name__ == '__main__':

    unittest.main()