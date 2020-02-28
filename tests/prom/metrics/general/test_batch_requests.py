from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.batch_requests import BatchRequests, TOTAL_COUNT
from tests.helpers import setUpApp, with_context


class TestBatchRequest(TestCase):

    def setUp(self):
        setUpApp(self)

    @with_context
    def test_should_collect(self):
        test_data = {TOTAL_COUNT: 100}

        batch_requests = BatchRequests(CollectorRegistry())

        batch_requests.collect(self.app, rows=(_ for _ in [test_data]))

        samples = next(iter(batch_requests.metric.collect())).samples

        self.assertEqual(test_data[TOTAL_COUNT], next(iter(samples)).value)
