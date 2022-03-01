from typing import List

from neo4j.graph import Node

from records.abstract_migration_record import AbstractMigrationRecord


class AspxMigrationRecord(AbstractMigrationRecord):
    """
    ASPX Migration
    """

    def __init__(self, node: Node):
        super().__init__()
        self.__node = node

        self.aip_type = ""
        self.name = ""
        self.full_name = ""
        self.attached_cs_file = ""
        self.attached_cs_fullname = ""
        self.cs_complexity: float = 0
        self.cs_loc: float = 0
        self.html_loc: float = 0

        # Difficulty related
        self.difficulty_segment = 1

    @staticmethod
    def get_headers() -> List:
        return [
            "Object Type",
            "Object Name",
            "Object Fullname",
            "Attached CS File name",
            "Attached CS File full name",
            "CS Code Complexity",
            "CS Code Loc",
            "Html Code Loc",
            "Difficulty Normalized",
            "Difficulty Segment",
            "Time Estimation",
            "Cost Estimation"
        ]

    def get_record(self):
        return [
            self.aip_type,
            self.name,
            self.full_name,
            self.attached_cs_file,
            self.attached_cs_fullname,
            self.cs_complexity,
            self.cs_loc,
            self.html_loc,
            self.get_normalized_score(),
            self.get_difficulty_segment(),
            self.get_time_estimate(),
            self.get_cost_estimate()
        ]

    def get_difficulty_score(self):
        """
        Compute the difficulty factor
        :return:
        """
        return self.cs_loc * self.cs_complexity + self.html_loc

    def get_time_estimate(self):
        """
        Get time estimate
        :return:
        """
        cs_loc_cost = float(self.time_manager.get_time_factor("CSHARP", "rewrite", "loc"))
        html_loc_cost = float(self.time_manager.get_time_factor("HTML", "rewrite", "loc"))

        cs_cost = self.cs_loc * cs_loc_cost * self.get_normalized_score()
        html_loc_cost = self.html_loc * html_loc_cost

        return cs_cost + html_loc_cost

    def get_cost_estimate(self):
        """
        Get cost estimate
        :return:
        """
        return self.get_time_estimate() * self.cost_manager.get_cost_per_person_hour()
