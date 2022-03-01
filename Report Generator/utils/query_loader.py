import logging
import os
from typing import Any, List, Dict

import yaml

from db.neo4j.neo4j_al import Neo4jAl
from definitions import ROOT_DIR
from interfaces.query.cypher_query import CypherQuery
from logger import Logger
from metaclass.SingletonMeta import SingletonMeta
from utils.folder.folder_utils import FolderUtils


class QueryLoader(metaclass=SingletonMeta):
    """
    Loads the query from the configuration file
    """

    query_folder = os.path.join(ROOT_DIR, 'configuration/cypher/')

    def __init__(self):
        self.__logger = Logger.get_logger("Neo4j Query Loader")
        self.__configuration: Dict[str, Dict[str, CypherQuery]] = dict()
        self.__neo4j_al = Neo4jAl()

        # List and load files
        files = self.__list_file()
        self.__logger.info("{0} .yml files were discovered.".format(len(files)))

        for f in files:
            self.__load_file(f)

        self.__logger.info("{0} cypher sections loaded.".format(len(self.__configuration)))

    def __list_file(self) -> List[str]:
        """
            List yml files
            :return: the list of files containing queries
        """
        return FolderUtils.list_folder(self.query_folder, True, ".yml")

    def __load_file(self, file_path: str):
        """
            Process a Yml file, and return a list of query
            :param file_path: File to process
            :return: The list of query discovered
        """
        # Verify yml
        if not file_path.endswith(".yml"):
            raise FileNotFoundError("Cannot process non-yml files.")

        # open the file and get the configuration
        yml_conf: Any = None
        with open(file_path, "r") as stream:
            try:
                yml_conf = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                self.__logger.error("Failed to process query configuration file at '{0}'.".format(file_path), e)
                return

        # If file is empty
        if yml_conf is None:
            self.__logger.error("Query file at '{0}' is empty.".format(file_path))
            return

        # Parse the configuration and build the list
        for section_name in yml_conf.keys():
            try:
                # Load the section
                # if section is empty remove
                if len(yml_conf[section_name]) == 0:
                    self.__logger.warning("Sections {0} is empty.".format(section_name))
                    continue

                # Else process the section
                if section_name not in self.__configuration.keys():
                    self.__configuration[section_name] = dict()
                else:
                    self.__logger.warning("Sections {0} already exist and will be overloaded.".format(section_name))

                queries = self.__load_section(section_name, yml_conf[section_name])
                self.__configuration[section_name].update(queries)

            except Exception as e:
                self.__logger.error("Sections {0} has been ignored.".format(section_name), e)

        return self.__configuration

    def __load_section(self, name: str, content: any) -> Dict[str, any]:
        """
        Load a section containing queries
        :param name: Name of the section
        :param content:  Content of the section
        :return:
        """
        ret_val = {}
        for query_name in content.keys():
            try:
                # Build the query from the yaml file
                query = self.build_query(content[query_name])
                ret_val[query_name] = query
            except:
                self.__logger.error("Query {0} has been ignored (Section : {1}).".format(query_name, query_name), e)

        return ret_val

    def __get_params(self, obj, params, default=None) -> Any:
        """
        Get the parameters of the object
        :param obj:  Object
        :param params: Parameters to get
        :param default: Default value
        :return:
        """
        try:
            return obj[params]
        except:
            return default

    def build_query(self, raw_query) -> CypherQuery:
        """
        Build the query based on its YAML declaration
        :param raw_query: Raw query to process
        :return: CypherQuery Class
        """
        if not raw_query["query"]:
            raise KeyError("The query is malformed. Missing query")

        params = self.__get_params(raw_query, "params", [])
        anchors = self.__get_params(raw_query, "anchors", [])
        returns = self.__get_params(raw_query, "return", None)

        return CypherQuery(raw_query["query"], anchors, params, returns)

    def get_query(self, section: str, name: str) -> CypherQuery:
        """
        Get the query and return a wrapped class of it
        :param section: Name of the section containing the query
        :param name: Name of the query to extract
        :return: The CypherQuery
        """

        # Verify the configuration
        if section not in self.__configuration.keys():
            raise KeyError("The section {0} does not exist in the configuration".format(section))

        if name not in self.__configuration[section].keys():
            raise KeyError("The section {0} does not contain query with name {1}".format(section, name))

        try:
            # Build and return the quer
            return self.__configuration[section][name]
        except KeyError as e:
            logging.error("Failed to build query with name {0} in section {1}".format(name, section), e)
            raise ValueError("Failed to build query with name {0}. Check the logs".format(name))

    def execute_query(self, section: str, name: str, params: Dict = None, anchors: Dict = None) -> list:
        """
        Execute the query and get the results
        :param section: Section to query
        :param name: Name of the query
        :param params: Parameters of the query
        :param anchors: Anchors to apply e.g. : ({ APPLICATION : "test" })
        :return:
        """

        query = self.get_query(section, name)
        for key in anchors.keys():
            query.replace_anchors({key: anchors[key]})

        # Execute
        return self.__neo4j_al.execute(query, params)
