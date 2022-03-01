import logging
from typing import Any

from neo4j import GraphDatabase

from interfaces.query.cypher_query import CypherQuery
from metaclass.SingletonMeta import SingletonMeta
from utils.configuration.neo4j_connection_info import Neo4jConnectionConfiguration
from utils.logger import Logger


class Neo4jAl(metaclass=SingletonMeta):
    """
    Class handling the connection to the Neo4j Database
    """

    def __init__(self):
        """
        Initialize the database access and initialize the connection with the configuration file
        """
        super(Neo4jAl, self).__init__()

        self.__logger = Logger.get_logger("Neo4j Access Layer")
        self.__neo4j_info = Neo4jConnectionConfiguration()

        # Read imaging configuration
        url = self.__neo4j_info.get_url()
        username = self.__neo4j_info.get_user()
        password = self.__neo4j_info.get_password()
        encryption = self.__neo4j_info.get_encryption_level()

        logging.info("Connecting to Neo4j Database : {0} (Encryption: {1} )".format(url, encryption))
        # Init connection
        try:
            self.__graph_database = GraphDatabase.driver(url, auth=(username, password), encrypted=encryption)
        except Exception as e:
            self.__logger.error("Failed to connect to the remote Neo4j database...", e)
            raise ConnectionError("Failed to connect to {0}".format(url))

    def __query_builder(self, query: CypherQuery, params: dict):
        """
        Build the query concatenating query string and params in a callback
        :param query: Query to run
        :param params: Parameters of the query
        :return: Lambda function to be executed in a session
        """

        def callback(tx):
            results = tx.run(query.get_query(), **params)
            return results

        return lambda tx: callback(tx)

    def __get_result(self, row, values: list or str) -> Any:
        """
        Extract the results
        :param row: Row to treat
        :param values: List of values to extract
        :return:
        """
        if len(values) == 1:
            return row[values[0]]
        elif isinstance(values, str):
            return row[values]
        else:
            ret_val = []
            for val in values:
                ret_val.append(row[val])
            return ret_val

    def execute(self, query: CypherQuery, params: dict = {}) -> list:
        """
        Run a query on the Neo4j database
        :param query: Query to run
        :param params: Parameters of the query as a map
        :return:
        """
        # Test query
        query.verify_params(params)

        # Run query
        records = []
        with self.__graph_database.session() as session:
            results = list(session.run(query.get_query(), params))

            # Get records
            for rec in results:
                ret_val = self.__get_result(rec, query.get_return_value())
                records.append(ret_val)

        return records
