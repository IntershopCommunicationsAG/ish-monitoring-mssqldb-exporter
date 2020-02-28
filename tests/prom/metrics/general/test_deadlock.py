from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.dead_lock import Deadlock, TOTAL_COUNT
from tests.helpers import setUpApp, with_context


class TestDeadlock(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {TOTAL_COUNT: 100}

        deadlock = Deadlock(CollectorRegistry())

        deadlock.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(deadlock.metric.collect())).samples

        self.assertEqual(test_data[TOTAL_COUNT], next(iter(samples)).value)
