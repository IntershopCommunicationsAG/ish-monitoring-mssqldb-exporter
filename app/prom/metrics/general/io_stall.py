from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

QUEUED_WRITE = '''stall_queued_write'''

QUEUED_READ = '''stall_queued_read'''

STALL = '''io_stall'''

WRITE = '''stall_write'''

READ = '''stall_read'''

NAME = '''name'''


class IOStall(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'mssql_io_stall'
            , 'Wait time (ms) of stall since last restart'
            , labelnames=['server', 'port', 'database', 'type']
            , registry=registry)

        self.metric_total = Gauge(
            'mssql_io_stall_total'
            , 'Wait time (ms) of stall since last restart'
            , labelnames=['server', 'port', 'database']
            , registry=registry)

        self.query = ('''
            SELECT
             cast(DB_Name(a.database_id) AS varchar) AS %s
             , max(io_stall_read_ms) AS %s
             , max(io_stall_write_ms) AS %s
             , max(io_stall) AS %s
             , max(io_stall_queued_read_ms) AS %s
             , max(io_stall_queued_write_ms) AS %s
            FROM sys.dm_io_virtual_file_stats(null, null) a
            INNER JOIN sys.master_files b ON a.database_id = b.database_id AND a.file_id = b.file_id
            GROUP BY a.database_id
        ''' % (NAME, READ, WRITE, STALL, QUEUED_READ, QUEUED_WRITE))

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:
                self.metric_total \
                    .labels(server=db_util.get_server(), port=db_util.get_port(), database=row[NAME]) \
                    .set(row[STALL])

            self._set_metric(row, READ)
            self._set_metric(row, WRITE)
            self._set_metric(row, QUEUED_READ)
            self._set_metric(row, QUEUED_WRITE)

    def _set_metric(self, row, stall_type):
        self.metric \
            .labels(server=db_util.get_server(), port=db_util.get_port(), database=row[NAME], type=stall_type) \
            .set(row[stall_type])
