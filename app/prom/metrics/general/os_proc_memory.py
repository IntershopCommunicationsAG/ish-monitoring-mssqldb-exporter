from prometheus_client import Gauge

from app.prom.database import util as db_util
from app.prom.metrics.abstract_metric import AbstractMetric

COUNT = '''count'''
PERCENTAGE = '''percentage'''
IN_USE = '''in_use'''
SPACE_COMMITTED = '''space_committed'''

class OsProcessMemory(AbstractMetric):
    def __init__(self, registry):
        """
        Initialize query and metrics
        """
        self.count_metric = Gauge(
            'mssql_page_fault_count'
            , '''Number of page faults since last restart'''
            , labelnames=['server', 'port']
            , registry=registry)
        self.memory_utilization_percentage_metric = Gauge(
            'mssql_memory_utilization_percentage'
            , '''Percentage of memory utilization'''
            , labelnames=['server', 'port']
            , registry=registry)
        self.virtual_address_space_committed_metric = Gauge(
            'mssql_virtual_address_space_committed_kb'
            , '''SQL Server resident memory size (AKA working set).'''
            , labelnames=['server', 'port']
            , registry=registry)
        self.physical_memory_in_use_metric = Gauge(
            'mssql_physical_memory_in_use_kb'
            , '''SQL Server committed virtual memory size.'''
            , labelnames=['server', 'port']
            , registry=registry)

        self.query = '''
            SELECT
             page_fault_count AS %s
             , memory_utilization_percentage AS %s
             , physical_memory_in_use_kb AS %s
             , virtual_address_space_committed_kb AS %s
            FROM sys.dm_os_process_memory
        ''' % (COUNT, PERCENTAGE, IN_USE, SPACE_COMMITTED)

        super().__init__()

    def collect(self, app, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        with app.app_context():
            row = next(rows)
            self.count_metric \
                .labels(server=db_util.get_server(), port=db_util.get_port()) \
                .set(row[COUNT])
            self.memory_utilization_percentage_metric \
                .labels(server=db_util.get_server(), port=db_util.get_port()) \
                .set(row[PERCENTAGE])
            self.physical_memory_in_use_metric \
                .labels(server=db_util.get_server(), port=db_util.get_port()) \
                .set(row[IN_USE])
            self.virtual_address_space_committed_metric \
                .labels(server=db_util.get_server(), port=db_util.get_port()) \
                .set(row[SPACE_COMMITTED])
