import unittest

from unittest import mock
from django_huey import task, periodic_task, lock_task, enqueue, restore, restore_all, restore_by_id, revoke\
,revoke_all, revoke_by_id, is_revoked, result, scheduled, on_startup, on_shutdown, pre_execute, post_execute\
,signal, disconnect_signal 

DECORATORS = [task, periodic_task, lock_task, enqueue, restore, restore_all, restore_by_id, revoke\
,revoke_all, revoke_by_id, is_revoked, result, scheduled, on_startup, on_shutdown, pre_execute, post_execute\
,signal, disconnect_signal]


class DecoratorsTest(unittest.TestCase):
    def make_test_decorator(self, decorator):
        with mock.patch('django_huey.get_queue') as obj:
            @decorator(queue='test_queue')
            def test_func():
                pass
            
            obj.assert_called_once_with("test_queue")

    def test_decorators(self):
        for decorator in DECORATORS:
            self.make_test_decorator(decorator)
