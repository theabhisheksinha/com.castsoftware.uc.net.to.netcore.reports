from interfaces.query.cypher_query import CypherQuery


class FlagQuery(CypherQuery):

    def __init__(self, query: str, anchors: list, params: list, returns: list, name: str = ""):
        super().__init__(query, anchors, params, returns, name)
        self.__title = ""
        self.__description = ""

    def get_title(self) -> str:
        """
        Get the title of the query
        :return: The Title
        """
        return self.__title

    def set_title(self, title: str):
        self.__title = title

    def set_description(self, description: str):
        self.__description = description

    def get_description(self) -> str:
        return self.__description
