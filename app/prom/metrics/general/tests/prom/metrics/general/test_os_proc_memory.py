from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.os_proc_memory import OsProcessMemory, COUNT, PERCENTAGE, IN_USE, SPACE_COMMITTED
from tests.helpers import setUpApp, with_context


class TestOsProcessMemory(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {COUNT: 100, PERCENTAGE: 90, IN_USE: 23, SPACE_COMMITTED: 50}

        os_process_memory = OsProcessMemory(CollectorRegistry())

        os_process_memory.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(os_process_memory.count_metric.collect())).samples
        self.assertEqual(test_data[COUNT], next(iter(samples)).value)

        samples = next(iter(os_process_memory.memory_utilization_percentage_metric.collect())).samples
        self.assertEqual(test_data[PERCENTAGE], next(iter(samples)).value)

        samples = next(iter(os_process_memory.physical_memory_in_use_metric.collect())).samples
        self.assertEqual(test_data[IN_USE], next(iter(samples)).value)

        samples = next(iter(os_process_memory.virtual_address_space_committed_metric.collect())).samples
        self.assertEqual(test_data[SPACE_COMMITTED], next(iter(samples)).value)
