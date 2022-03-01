from db.postgres.postgres_al import PostgresAL
from metaclass.SingletonMeta import SingletonMeta
from utils.logger import Logger


class NetToNetCoreDao(metaclass=SingletonMeta):
    """
    DAO for the net to net core report
    """

    def __init__(self):
        """
        Initialize the net core dao and instantiate the table
        """
        self.__logger = Logger.get_logger("Net to Net Dao")
        self.__postgres = PostgresAL()

