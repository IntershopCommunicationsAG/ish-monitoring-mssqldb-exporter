from unittest import TestCase

from prometheus_client.registry import CollectorRegistry

from app.prom.metrics.general.user_error import UserError, TOTAL_COUNT


class TestUserError(TestCase):
    def test_should_collect(self):
        test_data = {TOTAL_COUNT: 100}

        user_error = UserError(CollectorRegistry())

        user_error.collect(rows=(_ for _ in [test_data]))

        samples = next(iter(user_error.metric.collect())).samples

        self.assertEqual(test_data[TOTAL_COUNT], next(iter(samples)).value)
