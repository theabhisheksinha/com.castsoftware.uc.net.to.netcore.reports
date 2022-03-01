from typing import List

from neo4j.graph import Node

from records.abstract_migration_record import AbstractMigrationRecord


class ActionPlanRecord(AbstractMigrationRecord):
    """
        Record report
    """

    def __init__(self, node: Node):
        super(ActionPlanRecord, self).__init__()
        # Imaging information
        self.node = node
        self.name = ""
        self.full_name = ""
        self.parent_class = ""
        self.aip_type = ""

        # Compatibility
        self.compatible_net_core = ""
        self.compatible_standard_plus = ""
        self.compatible_net_core_plus = ""

        self.net_core_fullname = ""
        self.net_core_class = ""

        # Effort
        self.trans_in = 0
        self.essential_complexity = 0
        self.difficulty_factor = 1
        self.day_time_effort = 0.05 * 23.68
        self.fte_cost = 800

    @staticmethod
    def get_headers() -> List[str]:
        return [
            "Type",
            "Name",
            "FullName",
            "Parent",
            "Net Class Called",
            "Net Methods Called",
            "Compatible Dotnet Core platform with extensions",
            "Compatible Dotnet Core",
            "Compatible Dotnet Standard with extensions",
            "Effort Estimate",
            "Structural Priority"
        ]

    def get_difficulty_score(self):
        complexity = float(self.essential_complexity)
        self.difficulty_score = self.difficulty_factor * (1 + complexity)
        return self.difficulty_score

    def get_time_estimate(self):
        return self.get_difficulty_score() * self.day_time_effort

    def get_cost_estimate(self):
        return self.get_time_estimate() * self.fte_cost / 24

    def get_record(self):
        return [
            "SubObject",
            self.name,
            self.full_name,
            self.parent_class,
            self.net_core_class,
            self.net_core_fullname,
            self.compatible_net_core_plus,
            self.compatible_net_core,
            self.compatible_standard_plus,
            self.get_difficulty_score(),
            self.trans_in + 1
        ]
