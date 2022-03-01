# META
from numbers import Number
from metaclass.SingletonMeta import SingletonMeta

# Todo : Hardcoded
DAILY_RATE = 800

class CostManager(metaclass=SingletonMeta):
    """
    Cost Manager
    """

    def __init__(self):
        """
        Initialize the cost manager operation
        """
        pass

    def get_cost_per_person_hour(self):
        """
        Get the time modification factor for a technology
        :return:
        """

        return float(DAILY_RATE / 8)
