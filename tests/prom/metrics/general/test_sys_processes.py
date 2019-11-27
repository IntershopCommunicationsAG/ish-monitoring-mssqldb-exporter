from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.sys_processes import SysProcesses, DATABASE_NAME, CONNECTION_COUNT


class TestSysProcesses(TestCase):

    def test_should_collect(self):
        connection = SysProcesses(CollectorRegistry())
        test_data_1 = {DATABASE_NAME: 'test_1', CONNECTION_COUNT: 300}
        test_data_2 = {DATABASE_NAME: 'test_2', CONNECTION_COUNT: 1}

        connection.collect(rows=(_ for _ in [test_data_1, test_data_2]))

        samples = next(iter(connection.metric.collect())).samples
        iter_samples = iter(samples)

        self.assert_sample(iter_samples, test_data_1)
        self.assert_sample(iter_samples, test_data_2)

    def assert_sample(self, iter_samples, test_data):
        sample = next(iter_samples)
        self.assertEqual(test_data[CONNECTION_COUNT], sample.value)
        self.assertEqual(test_data[DATABASE_NAME], sample.labels['database'])
