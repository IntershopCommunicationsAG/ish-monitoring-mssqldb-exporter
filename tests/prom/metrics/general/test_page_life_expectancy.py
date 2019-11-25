from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.page_life_expectancy import PageLifeExpectancy, TOTAL_COUNT


class TestBatchRequest(TestCase):

    def test_should_collect(self):
        test_data = {TOTAL_COUNT: 100}

        page_life_expectancy = PageLifeExpectancy(CollectorRegistry())

        page_life_expectancy.collect(rows=(_ for _ in [test_data]))

        samples = next(iter(page_life_expectancy.metric.collect())).samples

        self.assertEqual(test_data[TOTAL_COUNT], next(iter(samples)).value)
