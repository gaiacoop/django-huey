import unittest

from unittest import mock
from django_huey import task, get_queue


class MultiQueueTest(unittest.TestCase):
    def setUp(self):
        
        get_queue('multi-1').flush()
        get_queue('multi-2').flush()

    def test_task_uses_specified_queue(self):
        
        @task(queue='multi-1')
        def some_fun():
            pass

        some_fun()

        queue1 = get_queue('multi-1')
        queue2 = get_queue('multi-2')
        self.assertEqual(len(queue1), 1)
        self.assertEqual(len(queue2), 0)
        
        @task(queue='multi-2')
        def some_other_fun():
            pass

        some_other_fun()

        queue1 = get_queue('multi-1')
        queue2 = get_queue('multi-2')
        self.assertEqual(len(queue1), 1)
        self.assertEqual(len(queue2), 1)


    def test_task_uses_default_queue_if_not_specified(self):
        @task()
        def some_default_func():
            pass

        some_default_func()

        queue1 = get_queue('multi-1')
        queue2 = get_queue('multi-2')
        self.assertEqual(len(queue1), 0)
        self.assertEqual(len(queue2), 1)
