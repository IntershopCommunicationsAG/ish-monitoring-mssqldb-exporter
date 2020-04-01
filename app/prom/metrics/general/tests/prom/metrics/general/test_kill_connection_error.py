from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.kill_connection_error import KillConnectionError, TOTAL_COUNT
from tests.helpers import setUpApp, with_context


class TestKillConnectionError(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {TOTAL_COUNT: 100}

        kill_connection_error = KillConnectionError(CollectorRegistry())

        kill_connection_error.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(kill_connection_error.metric.collect())).samples

        self.assertEqual(test_data[TOTAL_COUNT], next(iter(samples)).value)
