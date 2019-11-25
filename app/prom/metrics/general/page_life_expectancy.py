from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

TOTAL_COUNT = '''total_count'''


class PageLifeExpectancy(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'mssql_page_life_expectancy'
            , '''Indicates the minimum number of seconds a page will stay in the buffer pool on this node without references.
            The traditional advice from Microsoft used to be that the PLE should remain above 300 seconds'''
            , registry=registry)

        self.query = '''
        SELECT
         TOP 1 cntr_value AS %s
        FROM sys.dm_os_performance_counters WITH (nolock)
        WHERE counter_name = 'Page life expectancy'
        ''' % TOTAL_COUNT

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        self.metric.set(next(rows)[TOTAL_COUNT])
