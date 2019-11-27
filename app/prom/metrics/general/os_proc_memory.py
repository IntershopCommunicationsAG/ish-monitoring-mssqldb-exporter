from prometheus_client import Gauge

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
            , registry=registry)
        self.percentage_metric = Gauge(
            'mssql_memory_utilization_percentage'
            , '''Percentage of memory utilization'''
            , registry=registry)
        self.physical_memory_in_use_metric = Gauge(
            'mssql_virtual_address_space_committed_kb'
            , '''SQL Server resident memory size (AKA working set).'''
            , registry=registry)
        self.virtual_address_space_committed_metric = Gauge(
            'mssql_physical_memory_in_use_kb'
            , '''SQL Server committed virtual memory size.'''
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

    def collect(self, rows):
        """
        Collect from the query result
        :param rows: query result
        :return:
        """
        row = next(rows)
        self.count_metric.set(row[COUNT])
        self.percentage_metric.set(row[PERCENTAGE])
        self.physical_memory_in_use_metric.set(row[IN_USE])
        self.virtual_address_space_committed_metric.set(row[SPACE_COMMITTED])
