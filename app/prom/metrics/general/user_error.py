from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

TOTAL_COUNT = '''total_count'''


class UserError(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.metric = Gauge(
            'mssql_user_errors'
            , 'Number of user errors/sec since last restart'
            , labelnames=['server', 'port']
            , registry=registry)

        self.query = '''
        SELECT
         cntr_value AS %s
        FROM sys.dm_os_performance_counters
        WHERE counter_name = 'Errors/sec' AND instance_name = 'User Errors'
        ''' % TOTAL_COUNT

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            self.metric \
                .labels(server=db_util.get_server(), port=db_util.get_port()) \
                .set(next(rows)[TOTAL_COUNT])
