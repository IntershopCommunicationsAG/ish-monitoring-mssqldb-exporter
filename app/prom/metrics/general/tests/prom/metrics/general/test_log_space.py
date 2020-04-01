from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.log_space import LogSpace, TOTAL_LOG_SIZE, USED_LOG_SPACE, USED_LOG_SPACE_PERCENTAGE, USED_LOG_SPACE_SINCE_START
from tests.helpers import setUpApp, with_context


class TestLogSpace(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {TOTAL_LOG_SIZE: 100, USED_LOG_SPACE: 10, USED_LOG_SPACE_PERCENTAGE: 10, USED_LOG_SPACE_SINCE_START: 1}

        log_space = LogSpace(CollectorRegistry())

        log_space.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(log_space.total_log_size_in_bytes_metric.collect())).samples

        self.assertEqual(test_data[TOTAL_LOG_SIZE], next(iter(samples)).value)

        samples = next(iter(log_space.used_log_space_in_bytes_metric.collect())).samples

        self.assertEqual(test_data[USED_LOG_SPACE], next(iter(samples)).value)

        samples = next(iter(log_space.used_log_space_in_percentage_metric.collect())).samples

        self.assertEqual(test_data[USED_LOG_SPACE_PERCENTAGE], next(iter(samples)).value)

        samples = next(iter(log_space.log_space_in_bytes_since_last_backup_metric.collect())).samples

        self.assertEqual(test_data[USED_LOG_SPACE_SINCE_START], next(iter(samples)).value)
