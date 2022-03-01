from typing import List

from neo4j.graph import Node

from enums.artifact_type import ArtifactType
from enums.complexity_type import ComplexityType
from records.net.assembly_decommission_record import AssemblyDecommissionRecord
from repository.AbstractRepository import AbstractRepository
from repository.artifacts.artifacts_repository import ArtifactRepository
from utils.imaging.artifact_utils import ArtifactUtils
from utils.net.net_to_netcore_configuration import NetToNetCoreConfiguration


class NetMetricsRepository(AbstractRepository):
    """
    .Net metrics
    """

    def __init__(self, application: str):
        """
        Initialize the NetMetrics service
        :param application: Application to process
        """
        super(NetMetricsRepository, self).__init__(application)
        self.__net_configuration = NetToNetCoreConfiguration()

        # Artifacts
        self.__object_service = ArtifactRepository(self.get_application(), ArtifactType.OBJECT)
        self.__sub_object_service = ArtifactRepository(self.get_application(), ArtifactType.SUB_OBJECT)
        self.__raw_object_service = ArtifactRepository(self.get_application(), ArtifactType.RAW)


    def filter_compatibility_record(self, types: List[str]):
        """
        Filtered the compatibility records
        :param types:  Types to filter
        :return:
        """
        filtered = [x for x in types if x is not None]
        if 'Not supported' in filtered:
            return 'Not supported'
        elif len(filtered) == 0:
            return "No information"
        elif len(filtered) == 1:
            return filtered[0]
        else:
            return filtered

    def get_net_artifacts(self) -> List[Node]:
        """
        Get the list of .Net artifact to tag, using the type to get
        :return: The list of .Net artifacts
        """
        # Get the query to link an net object
        net_type = self.get_net_type()
        object_type = self.get_object_properties()

        query = self.query_service.get_query("migration", "get_artifacts_by_type")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "types": net_type,
            "prop_value": object_type
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def get_net_artifacts_object_like(self) -> List[Node]:
        """
        Get the list of .Net artifact to tag, using the type to get
        :return: The list of .Net artifacts
        """
        # Get the query to link an net object
        net_type = self.get_net_type()
        object_type = self.get_object_properties()

        query = self.query_service.get_query("migration", "get_artifacts_object_like_by_type")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "types": net_type,
            "prop_value": object_type
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def get_sub_object_list(self, node: Node) -> List[Node]:
        """
        Get the list of raw elements under
        :param node: Node to process
        :return:
        """
        query = self.query_service.get_query("migration", "get_sub_object_raw")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id,
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def get_net_type(self) -> List[str]:
        """
        Get the list of type supported
        :return:
        """
        return self.__net_configuration.get_supported_type()

    def get_object_properties(self) -> List[str]:
        """
        Get the list of type supported
        :return:
        """
        return self.__net_configuration.get_object_properties()

    def get_net_property_as_list(self) -> List[str]:
        """
        Get the list of net
        :return:
        """
        return self.__net_configuration.get_properties_as_list()
