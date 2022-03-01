from typing import List

from neo4j.graph import Node

from repository.AbstractRepository import AbstractRepository


class RazorMetricsRepository(AbstractRepository):

    def get_remote_function(self, node: Node) -> List[Node]:
        """
        Get the list of C# Methods called by a page
        :param node: Razor page
        :return:
        """
        res = self.query_service.execute_query("razor_blazor", "get_function_actions", anchors={
            "APPLICATION": self.get_application()
        }, params={
            "id": node.id
        })

        return res if len(res) >= 1 else []

