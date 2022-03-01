from neo4j.graph import Node

from enums.artifact_type import ArtifactType
from enums.complexity_type import ComplexityType
from repository.AbstractRepository import AbstractRepository


class ArtifactRepository(AbstractRepository):
    """
    Manage object and sub objects - Abstract
    """

    def __init__(self, application: str, artifact_type: ArtifactType):
        """
        Init Artifact Service
        :param application:  Name of the application
        """
        super(ArtifactRepository, self).__init__(application)
        self.__type = artifact_type.value[0]

    # Todo : Refactor upper limit
    def get_complexity_in(self, node: Node, complexity: ComplexityType, upper_limit: float = 1000):
        """
        Get the complexity of incoming objects for a node in the kb in the KB
        :param upper_limit: Cap the limit of complexity if needed ( deprecated )
        :param node: Object to get
        :param complexity: Complexity to get
        :return: The complexity of the objects
        """
        # Get the query to link an net object
        query = self.query_service.get_query(self.__type, "get_complexity_in")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id,
            "complexity": str(complexity.value[0]),
            "upper_limit": upper_limit
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else 0

    def get_complexity(self, node: Node, complexity: ComplexityType):
        """
            Get the complexity of an object in the KB
            :param node: Object to get
            :param complexity: Complexity to get
            :return: The complexity
            """
        # Get the query to link an net object
        query = self.query_service.get_query(self.__type, "get_complexity")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id,
            "complexity": str(complexity.value[0])
        }

        temp = query.get_query().replace("$id", str(node.id)).replace("$complexity", str(complexity.value[0]))
        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else 0

    def get_fan_in(self, node: Node):
        """
        Get the fan in of an object
        :param node: Node to get
        :return: Number of Artifact of the same type calling the element
        """
        # Get the query to link an net object
        query = self.query_service.get_query(self.__type, "get_fan_in")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else 0

    def get_parent(self, node: Node) -> Node or None:
        """
        Get the parent node of an artifact
        :param node: Node to get
        :return: Number of Artifact of the same type calling the element
        """
        # Get the query to link an net object
        query = self.query_service.get_query(self.__type, "get_parent")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else None

    def get_property_value(self, node: Node, property_name: str, default: any) -> Node or None:
        """
        Get the parent node of an artifact
        :param node: Node to get
        :return: Number of Artifact of the same type calling the element
        """
        # Get the query to link an net object
        query = self.query_service.get_query("artifacts", "get_property")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id,
            "property": property_name
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else default

    def get_property_under(self, node: Node, property_name: str) -> []:
        """
        Get the list of value for the properties under the specified node
        :param property_name: Name of the property to get
        :param node: Node to get
        :return: List of value found for the properties
        """
        # Get the query to link an net object
        query = self.query_service.get_query("migration", "get_properties_under_raw")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id,
            "prop_value": property_name
        }

        # Execute
        debug = query.get_query().replace("$id", str(node.id)).replace("prop_value", "\"" + str(property_name) + "\"")
        res = self._neo4j_al.execute(query, parameters)
        ret_val = list(res[0]) if len(res) >= 1 and len(res[0]) >= 1 else []
        return ret_val

    def get_transaction_number(self, node: Node):
        """
        Get the number of transaction using this artifact
        :param node: Node to get
        :return: Number of transaction
        """
        # Get the query to link an net object
        query = self.query_service.get_query(self.__type, "get_transaction_number")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Declare parameters
        parameters = {
            "id": node.id
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        return res[0] if len(res) >= 1 else 0
