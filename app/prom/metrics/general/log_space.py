from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

TOTAL_LOG_SIZE = '''total_log_size_in_bytes'''
USED_LOG_SPACE = '''used_log_space_in_bytes'''
USED_LOG_SPACE_PERCENTAGE = '''used_log_space_in_percent'''
USED_LOG_SPACE_SINCE_START = '''log_space_in_bytes_since_last_backup'''


class LogSpace(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.total_log_size_in_bytes_metric = Gauge(
            'mssql_log_total_size_in_bytes'
            , '''Total log size in bytes'''
            , registry=registry)
        self.used_log_space_in_bytes_metric = Gauge(
            'mssql_log_used_space_in_bytes'
            , '''Used log space in bytes'''
            , registry=registry)
        self.used_log_space_in_percentage_metric = Gauge(
            'mssql_log_used_space_in_percentage'
            , '''Used log space in percentage'''
            , registry=registry)
        self.log_space_in_bytes_since_last_backup_metric = Gauge(
            'mssql_log_space_in_bytes_since_last_backup'
            , '''Log space in bytes since last backup'''
            , registry=registry)

        self.query = '''
        SELECT
         total_log_size_in_bytes AS %s
         , used_log_space_in_bytes AS %s
         , used_log_space_in_percent AS %s
         , log_space_in_bytes_since_last_backup AS %s
        FROM sys.dm_db_log_space_usage
        ''' % (TOTAL_LOG_SIZE, USED_LOG_SPACE, USED_LOG_SPACE_PERCENTAGE, USED_LOG_SPACE_SINCE_START)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        row = next(rows)
        self.total_log_size_in_bytes_metric.set(row[TOTAL_LOG_SIZE])
        self.used_log_space_in_bytes_metric.set(row[USED_LOG_SPACE])
        self.used_log_space_in_percentage_metric.set(row[USED_LOG_SPACE_PERCENTAGE])
        self.log_space_in_bytes_since_last_backup_metric.set(row[USED_LOG_SPACE_SINCE_START])
