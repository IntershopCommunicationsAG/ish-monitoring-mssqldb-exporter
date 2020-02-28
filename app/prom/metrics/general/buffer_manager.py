from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

COUNTER_NAME = '''counter_name'''
VALUE = '''value'''


class BufferManager(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'mssql_buffer_manager'
            , 'Several buffer manager counters of SQL Server.'
            , labelnames=['server', 'port', 'counter_name']
            , registry=registry)

        self.query = ('''
            SELECT
             counter_name AS %s
             , cntr_value AS %s
            FROM sys.dm_os_performance_counters
            WHERE counter_name IN (
             'Page reads/sec'
             , 'Page writes/sec'
             , 'Lazy writes/sec'
             , 'Buffer cache hit ratio'
             , 'Page life expectancy'
            )
            AND object_name LIKE '%%Buffer Manager%%'
        ''' % (COUNTER_NAME, VALUE))

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:
                self.metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), counter_name=self.cleanName(row[COUNTER_NAME])) \
                    .set(row[VALUE])
