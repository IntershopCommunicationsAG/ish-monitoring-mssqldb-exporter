from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

DATABASE_NAME = '''database_name'''
VALUE = '''value'''

class LogGrowths(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'mssql_log_growths'
            , '''Total number of times the transaction log for the database has been expanded since last restart.'''
            , labelnames=['database']
            , registry=registry)

        self.query = '''
        SELECT rtrim(instance_name) AS %s, cntr_value AS %s
        FROM sys.dm_os_performance_counters
        WHERE counter_name = 'Log Growths'
         AND instance_name <> '_Total'
        ''' % (DATABASE_NAME, VALUE)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(database=row[DATABASE_NAME]) \
                .set(row[VALUE])


