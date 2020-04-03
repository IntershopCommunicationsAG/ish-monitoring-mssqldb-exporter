from operator import attrgetter
from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.io_stall import IOStall, NAME, AVG_READ, MAX_READ, AVG_WRITE, MAX_WRITE, AVG_IO_STALL, MAX_IO_STALL, QUEUED_READ, QUEUED_WRITE
from tests.helpers import setUpApp, with_context


class TestIOStall(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {NAME: 'test_1', AVG_READ: 300, MAX_READ: 100, AVG_WRITE: 300, MAX_WRITE: 100, AVG_IO_STALL: 500, MAX_IO_STALL: 1000, QUEUED_READ: 100, QUEUED_WRITE: 100}

        io_stall = IOStall(CollectorRegistry())

        io_stall.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(io_stall.metric.collect())).samples
        samples.sort(key=lambda sample: sample[1]['type'], reverse=False)
        iter_samples = iter(samples)

        self.assert_sample_metric(iter_samples, test_data, AVG_IO_STALL)
        self.assert_sample_metric(iter_samples, test_data, AVG_READ)
        self.assert_sample_metric(iter_samples, test_data, AVG_WRITE)
        self.assert_sample_metric(iter_samples, test_data, MAX_IO_STALL)
        self.assert_sample_metric(iter_samples, test_data, MAX_READ)
        self.assert_sample_metric(iter_samples, test_data, MAX_WRITE)
        self.assert_sample_metric(iter_samples, test_data, QUEUED_READ)
        self.assert_sample_metric(iter_samples, test_data, QUEUED_WRITE)

    def assert_sample_metric(self, iter_samples, test_data, stall_type):
        sample = next(iter_samples)
        self.assertEqual(test_data[stall_type], sample.value)
        self.assertEqual(test_data[NAME], sample.labels['database'])
