import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
from tests.tests_config import *
from tests.tests_decorators import *
from tests.tests_multiqueue import *
