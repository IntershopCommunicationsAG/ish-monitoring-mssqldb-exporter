from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

UPTIME = '''uptime'''


class Uptime(AbstractMetric):

    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'mssql_uptime'
            , 'Gauge metric with uptime in days of the Instance.'
            , labelnames=['server', 'port']
            , registry=registry)

        self.query = '''
        SELECT DATEDIFF(day, sqlserver_start_time, GETDATE ()) AS %s
        FROM sys.dm_os_sys_info
        ''' % UPTIME

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
                .set(next(rows)[UPTIME])
