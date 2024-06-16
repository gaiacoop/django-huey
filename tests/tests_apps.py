import unittest
import django


class DjangoHueyConfigTests(unittest.TestCase):
    def test_djangohuey_config_with_monitor_installed(self):
        django.setup()
