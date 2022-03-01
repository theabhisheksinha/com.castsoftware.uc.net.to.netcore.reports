import logging
import os
from typing import List, Dict

import yaml

from definitions import ROOT_DIR
from interfaces.net.net_core_property import NetCoreProperty
from metaclass.SingletonMeta import SingletonMeta


class NetToNetCoreConfiguration(metaclass=SingletonMeta):
    """
    Load properties related to AIP and .net core migration
    """

    query_file = os.path.join(ROOT_DIR, 'configuration/net/net_to_netcore.yml')

    def __init__(self):
        with open(self.query_file, "r") as stream:
            try:
                self.__configuration = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                logging.error("Failed to process net_to_netcore configuration file at {0}".format(self.query_file), e)
                raise FileNotFoundError("Failed to process query file at {0}.".format(self.query_file))

    def get_supported_type(self) -> List[str]:
        """
        Get the list of supported type
        :return:
        """
        # Verify section
        if not self.__configuration["migration"]:
            raise KeyError("Section with name 'migration' does not exist")

        # Verify element in section
        if not self.__configuration["migration"]["supported_type"]:
            raise KeyError("Element with name 'supported_type' does not exist in section 'migration'")

        return self.__configuration["migration"]["supported_type"]

    def get_properties_as_list(self) -> List[str]:
        """
        Get the list of properties name
        :return:
        """
        properties = self.get_properties()
        it = map(lambda x: x.get_property(), properties)
        return list(it)

    def get_properties_as_map(self) -> Dict[str, NetCoreProperty]:
        """
        Get the list of properties name
        :return: Map with key as the name
        """
        properties = self.get_properties()
        dictionary = {}
        for prop in properties:
            dictionary[prop.get_property()] = prop
        return dictionary

    def get_properties(self) -> List[NetCoreProperty]:
        """
        Get the list of .Net to Net core properties in the configuration file
        :return:  The properties as a list
        """
        # Verify section
        if not self.__configuration["migration"]:
            raise KeyError("Section with name 'migration' does not exist")

        # Verify element in section
        if not self.__configuration["migration"]["properties_to_migrate"]:
            raise KeyError("Element with name 'properties_to_migrate' does not exist in section 'migration'")

        properties = []
        it = None

        # Iterate through the configuration and build list
        for elem in self.__configuration["migration"]["properties_to_migrate"]:
            it = NetCoreProperty(elem["property"], elem["name"], elem["description"])
            properties.append(it)

        return properties

    def get_object_properties(self) -> List[str]:
        """
        Get the list of .Net to Net core properties in the configuration file
        :return:  The properties as a list
        """
        # Verify section
        if not self.__configuration["migration"]:
            raise KeyError("Section with name 'migration' does not exist")

        # Verify element in section
        if not self.__configuration["migration"]["object_properties"]:
            raise KeyError("Element with name 'object_properties' does not exist in section 'migration'")

        return self.__configuration["migration"]["object_properties"]
