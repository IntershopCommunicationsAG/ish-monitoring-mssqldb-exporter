from abc import ABCMeta, abstractmethod


class AbstractMetric:
    """
    Abstract class for prom.
    This class defines the API interface for various types of prom.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """
        Empty constructor for now. Every derived class would be forced to create one.
        Should initialize query and metric
        """
    @abstractmethod
    def collect(self, rows):
        """
        Collect prom from MSSQL and set prometheus
        :param rows: sql result
        :return:
        """
        pass
