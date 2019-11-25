from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.os_sys_memory import OsSysMemory, TOTAL_MEM, AVAILABLE_MEM, AVAILABLE_PAGE, TOTAL_PAGE


class TestOsSysMemory(TestCase):
    def test_should_collect(self):
        test_data = {TOTAL_MEM: 100, AVAILABLE_MEM: 10, TOTAL_PAGE: 10, AVAILABLE_PAGE: 1}

        os_sys_mem = OsSysMemory(CollectorRegistry())

        os_sys_mem.collect(rows=(_ for _ in [test_data]))

        samples = next(iter(os_sys_mem.total_mem_metric.collect())).samples

        self.assertEqual(test_data[TOTAL_MEM], next(iter(samples)).value)

        samples = next(iter(os_sys_mem.available_mem_metric.collect())).samples

        self.assertEqual(test_data[AVAILABLE_MEM], next(iter(samples)).value)

        samples = next(iter(os_sys_mem.total_page_metric.collect())).samples

        self.assertEqual(test_data[TOTAL_PAGE], next(iter(samples)).value)

        samples = next(iter(os_sys_mem.available_page_metric.collect())).samples

        self.assertEqual(test_data[AVAILABLE_PAGE], next(iter(samples)).value)
