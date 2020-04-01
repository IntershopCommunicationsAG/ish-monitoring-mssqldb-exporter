from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

DATABASE_NAME = '''database_name'''
TOTAL_LOG_SIZE = '''total_log_size_in_bytes'''
USED_LOG_SPACE = '''used_log_space_in_bytes'''
USED_LOG_SPACE_PERCENTAGE = '''used_log_space_in_percent'''


class LogSpace(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.total_log_size_in_bytes_metric = Gauge(
            'mssql_log_total_size_in_bytes'
            , '''Total log size in bytes'''
            , labelnames=['server', 'port', 'database']
            , registry=registry)
        self.used_log_space_in_bytes_metric = Gauge(
            'mssql_log_used_space_in_bytes'
            , '''Used log space in bytes'''
            , labelnames=['server', 'port', 'database']
            , registry=registry)
        self.used_log_space_in_percentage_metric = Gauge(
            'mssql_log_used_space_in_percentage'
            , '''Used log space in percentage'''
            , labelnames=['server', 'port', 'database']
            , registry=registry)

        self.query = '''
            SELECT
             rtrim(lu.instance_name) AS %s
             , ls.cntr_value AS %s
             , lu.cntr_value AS %s
             , CAST(CAST(lu.cntr_value AS FLOAT) / CAST(ls.cntr_value AS FLOAT) AS DECIMAL(18,2)) * 100 AS %s
            FROM sys.dm_os_performance_counters AS lu WITH (NOLOCK)
            INNER JOIN sys.dm_os_performance_counters AS ls WITH (NOLOCK)
            ON lu.instance_name = ls.instance_name
            WHERE lu.counter_name LIKE N'Log File(s) Used Size (KB)%%'
            AND ls.counter_name LIKE N'Log File(s) Size (KB)%%'
            AND ls.cntr_value > 0
            AND ls.instance_name <> '_Total'
        ''' % (DATABASE_NAME, TOTAL_LOG_SIZE, USED_LOG_SPACE, USED_LOG_SPACE_PERCENTAGE)

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:
                self.total_log_size_in_bytes_metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), database=row[DATABASE_NAME]) \
                    .set(row[TOTAL_LOG_SIZE])
                self.used_log_space_in_bytes_metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), database=row[DATABASE_NAME]) \
                    .set(row[USED_LOG_SPACE])
                self.used_log_space_in_percentage_metric \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), database=row[DATABASE_NAME]) \
                    .set(row[USED_LOG_SPACE_PERCENTAGE])
