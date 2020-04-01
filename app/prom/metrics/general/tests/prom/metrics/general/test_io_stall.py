from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.io_stall import IOStall, NAME, READ, WRITE, STALL, QUEUED_READ, QUEUED_WRITE
from tests.helpers import setUpApp, with_context


class TestIOStall(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {NAME: 'test_1', READ: 300, WRITE: 100, STALL: 500, QUEUED_READ: 100, QUEUED_WRITE: 100}

        io_stall = IOStall(CollectorRegistry())

        io_stall.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(io_stall.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample_metric(iter_samples, test_data, READ)
        self.assert_sample_metric(iter_samples, test_data, WRITE)
        self.assert_sample_metric(iter_samples, test_data, QUEUED_READ)
        self.assert_sample_metric(iter_samples, test_data, QUEUED_WRITE)

        samples = next(iter(io_stall.metric_total.collect())).samples
        iter_samples = iter(samples)
        self.assert_sample_metric_total(iter_samples, test_data)

    def assert_sample_metric(self, iter_samples, test_data, stall_type):
        sample = next(iter_samples)
        self.assertEqual(test_data[stall_type], sample.value)
        self.assertEqual(test_data[NAME], sample.labels['database'])

    def assert_sample_metric_total(self, iter_samples, test_data_1):
        sample = next(iter_samples)
        self.assertEqual(test_data_1[STALL], sample.value)
        self.assertEqual(test_data_1[NAME], sample.labels['database'])
