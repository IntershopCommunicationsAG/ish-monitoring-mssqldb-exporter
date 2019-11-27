from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

COUNTER_NAME = '''counter_name'''
VALUE = '''value'''


class PerformanceCounters(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge('mssql_performance_counters',
                        'Several performance counters of SQL Server.',
                        labelnames=['counter_name'],
                        registry=registry)

        self.query = ('''
        SELECT
         counter_name AS %s
         , cntr_value AS %s
        FROM sys.dm_os_performance_counters
        WHERE counter_name IN (
         'Target Server Memory (KB)'
         , 'Total Server Memory (KB)'
         , 'Lock Blocks'
         , 'Lock Blocks Allocated'
         , 'Lock Memory (KB)'
         , 'Lock Owner Blocks'
         , 'Connection Memory (KB)'
         , 'User Connections'
        )
        ''' % (COUNTER_NAME, VALUE))

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(counter_name=self.cleanName(row[COUNTER_NAME])) \
                .set(row[VALUE])
