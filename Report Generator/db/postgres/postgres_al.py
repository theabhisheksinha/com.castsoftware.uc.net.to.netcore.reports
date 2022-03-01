import logging

import psycopg2
from metaclass.SingletonMeta import SingletonMeta
from utils.configuration.default_configuration import DefaultConfiguration


class PostgresAL(metaclass=SingletonMeta):
    """
    Postgres Server communication file
    """

    def __init__(self):
        """
        Initialize the postgres database access with the configuration file
        """
        super(PostgresAL, self).__init__()
        self.__config = DefaultConfiguration()

        # Read imaging configuration
        host = str(self.__config.get_value("postgres", "host"))
        port = str(self.__config.get_value("postgres", "port"))
        database = str(self.__config.get_value("postgres", "database"))
        username = str(self.__config.get_value("postgres", "username"))
        password = str(self.__config.get_value("postgres", "password"))

        address = "{0}:{1}".format(host, port)

        logging.info("Connecting to Postgres Database : {0} (Database: {1} )".format(host, database))
        # Init connection
        try:
            self.__postgres_db = psycopg2.connect(
                host=address,
                database=database,
                user=username,
                password=password)

        except Exception as e:
            logging.error("Failed to connect to the remote postgres database...", e)
            raise ConnectionError("Failed to connect to {0}".format(host))

    def execute(self, query: str, **args) -> list:
        """
        Execute the SQL statement along with arguments against the database
        :param query: Query to execute
        :param args:  Arguments
        :return:
        """
        records = []

        # Open cursor
        with  self.__postgres_db.cursor() as cur:
            # Log
            logging.info("Executing SQL query: {0}.".format(query))

            # Execute the statement
            cur.execute(query, args)
            row = cur.fetchone()

            while row is not None:
                records.append(row)
                row = cur.fetchone()  # Fetch next one

        return records

    def execute_async(self, callback, query: str, **args) -> None:
        """
        Execute the SQL statement along with arguments against the database
        :param callback: Callback function to execute
        :param query: Query to execute
        :param args:  Arguments
        :return:
        """
        # Open cursor
        with  self.__postgres_db.cursor() as cur:
            # Log
            logging.info("Executing SQL query: {0}.".format(query))

            # Execute the statement
            cur.execute(query, args)
            row = cur.fetchone()

            while row is not None:
                callback(row)  # Callback on row
                row = cur.fetchone()  # Fetch next one
