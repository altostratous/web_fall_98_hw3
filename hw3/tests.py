from django.test import TestCase

from hw3.models import Virus, EvenMicrosecondObject

from django.db import connection
from threading import Thread


class TestThread(Thread):

    def run(self):
        super().run()

        connection.close()


class Test(TestCase):

    def test_virus_copy(self):

        for _ in range(3):
            Virus.grow_one_generation()

        self.assertEqual(
            Virus.objects.filter(copied_from_id=1).count(),
            Virus.objects.get(id=1).number_of_copies,
        )

    def test_odd_micro_second(self):

        threads = []
        to_assert_evens = []
        for _ in range(100):

            def create():
                EvenMicrosecondObject.create_one()

            thread = TestThread(target=create)
            threads.append(thread)
            thread.start()

            def sample():
                to_assert_evens.append(
                    sum(obj.created.microsecond for obj in EvenMicrosecondObject.objects.all())
                )

            thread = TestThread(target=sample())
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for to_assert_even in to_assert_evens:
            self.assertTrue(to_assert_even % 2 == 0)
