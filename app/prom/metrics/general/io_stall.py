from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

QUEUED_WRITE = '''stall_queued_write'''
QUEUED_READ = '''stall_queued_read'''

AVG_IO_STALL = '''avg_io_stall'''
MAX_IO_STALL = '''max_io_stall'''

AVG_WRITE = '''avg_stall_write'''
AVG_READ = '''avg_stall_read'''
MAX_WRITE = '''max_stall_write'''
MAX_READ = '''max_stall_read'''

NAME = '''name'''


class IOStall(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'mssql_io_stall'
            , 'Average and maximum Wait time (ms) of stall io since last restart'
            , labelnames=['server', 'port', 'database', 'type']
            , registry=registry)

        self.query = ('''
            SELECT
             CAST(DB_Name(a.database_id) AS varchar) AS %s
             , AVG(CASE WHEN num_of_reads = 0
                    THEN 0 ELSE (io_stall_read_ms / num_of_reads) END) AS %s
             , AVG(CASE WHEN num_of_writes = 0
                    THEN 0 ELSE (io_stall_write_ms / num_of_writes) END) AS %s
             , MAX(CASE WHEN num_of_reads = 0
                    THEN 0 ELSE (io_stall_read_ms / num_of_reads) END) AS %s
             , MAX(CASE WHEN num_of_writes = 0
                    THEN 0 ELSE (io_stall_write_ms / num_of_writes) END) AS %s
             , AVG(CASE WHEN num_of_reads + num_of_writes = 0
                    THEN 0 ELSE (io_stall / (num_of_reads + num_of_writes)) END) AS %s
             , MAX(CASE WHEN num_of_reads + num_of_writes = 0
                    THEN 0 ELSE (io_stall / (num_of_reads + num_of_writes)) END) AS %s
             , max(io_stall_queued_read_ms) AS %s
             , max(io_stall_queued_write_ms) AS %s
            FROM sys.dm_io_virtual_file_stats(null, null) a
            INNER JOIN sys.master_files b ON a.database_id = b.database_id AND a.file_id = b.file_id
            GROUP BY a.database_id
        ''' % (NAME, AVG_READ, AVG_WRITE, MAX_READ, MAX_WRITE, AVG_IO_STALL, MAX_IO_STALL, QUEUED_READ, QUEUED_WRITE))

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            for row in rows:
                self._set_metric(row, AVG_READ)
                self._set_metric(row, AVG_WRITE)
                self._set_metric(row, MAX_READ)
                self._set_metric(row, MAX_WRITE)
                self._set_metric(row, AVG_IO_STALL)
                self._set_metric(row, MAX_IO_STALL)
                self._set_metric(row, QUEUED_READ)
                self._set_metric(row, QUEUED_WRITE)

    def _set_metric(self, row, stall_type):
        self.metric \
            .labels(server=db_util.get_server(), port=db_util.get_port(), database=row[NAME], type=stall_type) \
            .set(row[stall_type])
