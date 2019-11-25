from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

TOTAL_COUNT = '''total_count'''


class BatchRequests(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'mssql_batch_requests'
            , '''Number of Transact-SQL command batches received per second.
            This statistic is affected by all constraints (such as I/O, number of users, cachesize,
            complexity of requests, and so on). High batch requests mean good throughput'''
            , registry=registry)

        self.query = '''
        SELECT
         TOP 1 cntr_value AS %s
        FROM sys.dm_os_performance_counters
        WHERE counter_name = 'Batch Requests/sec'
        ''' % TOTAL_COUNT

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        self.metric.set(next(rows)[TOTAL_COUNT])
