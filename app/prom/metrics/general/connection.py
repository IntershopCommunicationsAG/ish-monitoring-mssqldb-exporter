from prometheus_client import Gauge

from app.prom.metrics.abstract_metric import AbstractMetric

DATABASE_NAME = '''database_name'''

CONNECTION_COUNT = '''connection_count'''


class Connection(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """

        self.metric = Gauge(
            'mssql_connections'
            , 'Number of connections'
            , labelnames=['database', 'state',]
            , registry=registry)

        self.query = '''
        SELECT
         DB_NAME(sP.dbid) AS %s
         , COUNT(sP.spid) AS %s
        FROM sys.sysprocesses sP
        GROUP BY DB_NAME(sP.dbid)
        ''' % (DATABASE_NAME, CONNECTION_COUNT)

        super().__init__()

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        for row in rows:
            self.metric \
                .labels(database=row[DATABASE_NAME], state='current') \
                .set(row[CONNECTION_COUNT])
