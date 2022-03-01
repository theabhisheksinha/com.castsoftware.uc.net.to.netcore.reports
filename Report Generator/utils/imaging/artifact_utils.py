from neo4j.graph import Node


class ArtifactUtils:

    @staticmethod
    def get_label(node: Node, application: str) -> str:
        """
        Get the label of the node
        :param node: Node to retrieve
        :param application: Name of the application
        :return:
        """
        temp = [x for x in node.labels if x != application]
        return str(temp[0]) if len(temp) >= 1 else ""

    @staticmethod
    def get_name(node: Node) -> str:
        """
        Get the name of the artifact
        :param node: Node to explore
        :return:
        """
        return node.get("Name", "No name")

    @staticmethod
    def get_fullname(node: Node) -> str:
        """
        Get the fullname of the artifact
        :param node: Node to explore
        :return:
        """
        return node.get("FullName", "No fullname")

    @staticmethod
    def get_type(node: Node) -> str:
        """
        Get the type of the artifact
        :param node: Node to explore
        :return:
        """
        return node.get("Type", "No Type")
