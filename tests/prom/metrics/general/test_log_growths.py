from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.log_growths import LogGrowths, DATABASE_NAME, VALUE


class TestConnection(TestCase):

    def test_should_collect(self):
        log_growths = LogGrowths(CollectorRegistry())
        test_data_1 = {DATABASE_NAME: 'test_1', VALUE: 300}
        test_data_2 = {DATABASE_NAME: 'test_2', VALUE: 1}

        log_growths.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(log_growths.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample(iter_samples, test_data_1)
        self.assert_sample(iter_samples, test_data_2)

    def assert_sample(self, iter_samples, test_data):
        sample = next(iter_samples)
        self.assertEqual(test_data[VALUE], sample.value)
        self.assertEqual(test_data[DATABASE_NAME], sample.labels['database'])
