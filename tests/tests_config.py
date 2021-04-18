import unittest
from unittest.mock import patch
from huey import RedisHuey, MemoryHuey
from huey.exceptions import ConfigurationError
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
from django_huey.config import DjangoHueySettingsReader

class DjangoHueyTests(unittest.TestCase):
    def test_djangohuey_config_with_no_settings(self):
        config = DjangoHueySettingsReader(None)

        with self.assertRaises(ConfigurationError) as cm:
            config.configure()

        self.assertEqual('Error: HUEYS must be a dictionary', str(cm.exception))


    def test_djangohuey_configure_does_not_raise_error_when_both_settings_are_defined(self):
        HUEY = {
            'name': 'test',
            'immediate': True,
        }

        HUEYS = {
            'queuename': {
                'name': 'test',
                'immediate': True,
            }
        }
        config = DjangoHueySettingsReader(HUEYS)

        config.configure()

    def test_djangohuey_default_queue_when_queue_is_none(self):
        HUEYS = {
            'queuename': {
                'name': 'test',
                'immediate': True,
            }
        }
        config = DjangoHueySettingsReader(HUEYS)

        config.configure()

        with self.assertRaises(ConfigurationError) as cm:
            config.default_queue(None)

        self.assertEqual("""
If HUEYS is configured run_djangohuey must receive a --queue parameter
i.e.: 
python manage.py run_djangohuey --queue first
                """, str(cm.exception))

    def test_djangohuey_configure_when_hueys_setting_is_defined(self, *args):
        HUEYS = {
            'first': {
                'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
                'name': 'testname',  # Use db name for huey.
            },
            'mails': {
                'huey_class': 'huey.MemoryHuey',  # Huey implementation to use.
                'name': 'testnamememory',  # Use db name for huey.
            }
        }

        config = DjangoHueySettingsReader(HUEYS)

        config.configure()

        self.assertTrue(isinstance(config.default_queue('first'), RedisHuey))
        self.assertEqual(config.default_queue('first').name, 'testname')
        self.assertTrue(isinstance(config.default_queue('mails'), MemoryHuey))
        self.assertEqual(config.default_queue('mails').name, 'testnamememory')

    def test_djangohuey_configure_when_hueys_setting_is_an_object_raises_error(self, *args):
        HUEYS = object()

        config = DjangoHueySettingsReader(HUEYS)

        with self.assertRaises(ConfigurationError) as cm:
            config.configure()
        self.assertEqual('Error: HUEYS must be a dictionary', str(cm.exception))

if __name__ == '__main__':

    unittest.main()