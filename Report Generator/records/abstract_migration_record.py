from abc import ABC, abstractmethod

from business_metrics.cost_manager import CostManager
from business_metrics.time_manager import TimeManager


class AbstractMigrationRecord(ABC):
    """
    Record Abstract class
    """

    def __init__(self):
        """
        Default parameters for each records
        """
        self.cost_manager = CostManager()
        self.time_manager = TimeManager()

        self.normalized_score = 0
        self.difficulty_score = 0
        self.difficulty_segment = 0

    @abstractmethod
    def get_difficulty_score(self):
        pass

    @abstractmethod
    def get_time_estimate(self):
        pass

    @abstractmethod
    def get_cost_estimate(self):
        pass

    @abstractmethod
    def get_record(self):
        pass

    def set_difficulty_score(self, value: float):
        self.difficulty_score = value

    def set_normalized_score(self, value: float):
        self.normalized_score = value

    def get_normalized_score(self):
        return self.normalized_score

    def set_difficulty_segment(self, value: int):
        self.difficulty_segment = value

    def get_difficulty_segment(self) -> float:
        """
        Get the difficulty score
        :return: The segment number ( quartile )
        """
        return self.difficulty_segment
