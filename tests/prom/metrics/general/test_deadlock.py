from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.dead_lock import Deadlock, TOTAL_COUNT


class TestDeadlock(TestCase):
    def test_should_collect(self):
        test_data = {TOTAL_COUNT: 100}

        deadlock = Deadlock(CollectorRegistry())

        deadlock.collect(rows=(_ for _ in [test_data]))

        samples = next(iter(deadlock.metric.collect())).samples

        self.assertEqual(test_data[TOTAL_COUNT], next(iter(samples)).value)
