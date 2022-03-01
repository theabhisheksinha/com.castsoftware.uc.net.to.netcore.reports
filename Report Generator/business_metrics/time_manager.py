from utils.configuration.time_configuration import TimeConfiguration


class TimeManager:
    """
    Time Manager
    """

    def __init__(self):
        self.__time_configuration = TimeConfiguration()
        self.__default_value = self.__find_default()

    def __find_default(self) -> float:
        value = self.__time_configuration.get_value("time", "AVERAGE", "refactor", "loc")
        return value if value is not None else 0.005

    def get_time_factor(self, technology: str, change_type: str = "", unit="") -> float:
        """
        Get the time modification factor for a technology
        :param unit: Measurement unit ( Loc, Methods, Class )
        :param technology: Technology
        :param change_type: Type of the modification
        :return: The value found or average value for person-hour/defect
        """
        value = self.__time_configuration.get_value("time", technology, change_type, unit)
        return value if value is not None else 0.005
