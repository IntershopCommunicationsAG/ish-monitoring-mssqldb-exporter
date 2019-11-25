from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

COUNT = '''count'''
PERCENTAGE = '''percentage'''


class OsProcessMemory(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.count_metric = Gauge(
            'mssql_page_fault_count'
            , '''Number of page faults since last restart'''
            , registry=registry)
        self.percentage_metric = Gauge(
            'mssql_memory_utilization_percentage'
            , '''Percentage of memory utilization'''
            , registry=registry)

        self.query = '''
        SELECT
         page_fault_count AS %s
         , memory_utilization_percentage AS %s
        FROM sys.dm_os_process_memory
        ''' % (COUNT, PERCENTAGE)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        row = next(rows)
        self.count_metric.set(row[COUNT])
        self.percentage_metric.set(row[PERCENTAGE])
