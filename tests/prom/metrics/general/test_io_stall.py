from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.io_stall import IOStall, NAME, READ, WRITE, STALL, QUEUED_READ, QUEUED_WRITE


class TestIOStall(TestCase):
    def test_should_collect(self):
        test_data_1 = {NAME: 'test_1', READ: 300, WRITE: 100, STALL: 500, QUEUED_READ: 100, QUEUED_WRITE: 100}
        test_data_2 = {NAME: 'test_2', READ: 3, WRITE: 1, STALL: 5, QUEUED_READ: 1, QUEUED_WRITE: 1}

        io_stall = IOStall(CollectorRegistry())

        io_stall.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(io_stall.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metric(iter_samples, test_data_1, READ)
        self.assert_sample_metric(iter_samples, test_data_1, WRITE)
        self.assert_sample_metric(iter_samples, test_data_1, QUEUED_READ)
        self.assert_sample_metric(iter_samples, test_data_1, QUEUED_WRITE)
        self.assert_sample_metric(iter_samples, test_data_2, READ)
        self.assert_sample_metric(iter_samples, test_data_2, WRITE)
        self.assert_sample_metric(iter_samples, test_data_2, QUEUED_READ)
        self.assert_sample_metric(iter_samples, test_data_2, QUEUED_WRITE)

        samples = next(iter(io_stall.metric_total.collect())).samples
        iter_samples = iter(samples)
        self.assert_sample_metric_total(iter_samples, test_data_1)
        self.assert_sample_metric_total(iter_samples, test_data_2)

    def assert_sample_metric(self, iter_samples, test_data, stall_type):
        sample = next(iter_samples)
        self.assertEqual(test_data[stall_type], sample.value)
        self.assertEqual(test_data[NAME], sample.labels['database'])

    def assert_sample_metric_total(self, iter_samples, test_data_1):
        sample = next(iter_samples)
        self.assertEqual(test_data_1[STALL], sample.value)
        self.assertEqual(test_data_1[NAME], sample.labels['database'])
