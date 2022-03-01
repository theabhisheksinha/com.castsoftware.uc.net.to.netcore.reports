from typing import Any, List

from neo4j.graph import Node

# TODO : Remove this statements
from records.abstract_migration_record import AbstractMigrationRecord

UPPER_LIMIT_COMPLEXITY = 100
UPPER_LIMIT_STRUCTURE = 100

'''
"Use JSON.NET instead."
"Use AssemblyBuilder.DefineDynamicAssembly"
"Consider using System.Threading.AsyncLocal"
'''


class AssemblyDecommissionRecord(AbstractMigrationRecord):
    """
        Record report
    """

    def __init__(self, node: Node):
        super(AssemblyDecommissionRecord, self).__init__()
        self.node = node

        self.name = ""
        self.fullName = ""
        self.artifact_type = ""

        # Type related
        self.type = ""

        # Structure
        self.trans_in = 0

        self.recommended_change = ""

        self.cs_call_num = 0
        self.cs_methods_fullname = []
        self.cs_loc_in = 0
        self.cs_complexity_in = 0

        # Migration
        self.compatible_net_core = ""
        self.compatible_standard_plus = ""
        self.compatible_net_core_plus = ""

        # Parent
        self.parent = None


    @staticmethod
    def get_headers() -> List[str]:
        return [
            "Type",
            "Name",
            "FullName",
            "Parent",
            "Compatible Dotnet Core platform with extensions",
            "Compatible Dotnet Core",
            "Compatible Dotnet Standard with extensions",
            "Number of CS function using the assembly",
            "CS Function FullName",
            "Total CS loc to revise",
            "Average CS complexity",
            "Difficulty Normalized",
            "Difficulty Segment",
            "Time Estimation",
            "Cost Estimation",
            "Recommended Change",
            "Structural Impact"
        ]

    def get_record(self) -> List[Any]:
        """
        Get the records list
        :return: The list to be inserted in the CSV
        """
        return [
            self.type,

            self.name,
            self.fullName,
            self.parent,

            self.compatible_net_core_plus,
            self.compatible_net_core,
            self.compatible_standard_plus,

            self.cs_call_num,
            self.cs_methods_fullname,

            self.cs_loc_in,
            self.cs_complexity_in,

            self.get_normalized_score(),
            self.get_difficulty_segment(),

            self.get_time_estimate(),
            self.get_cost_estimate(),

            self.recommended_change,

            self.trans_in + 1
        ]

    def get_upper_limit(self) -> float or None:
        """
        Get the upper limit
        :return:
        """
        if self.recommended_change.startswith("Use"):
            return 1
        elif self.recommended_change.startswith("Consider"):
            return 2
        else:
            None

    def get_difficulty_score(self):
        """
        Calculate the effort complexity
        :return:
        """

        return self.cs_loc_in * self.cs_complexity_in

    def get_time_estimate(self):
        """
        Get time estimate
        :return:
        """
        cs_loc_cost = float(self.time_manager.get_time_factor("CSHARP", "rewrite", "loc"))

        return self.cs_loc_in * cs_loc_cost * self.get_normalized_score()

    def get_cost_estimate(self):
        """
        Get cost estimate
        :return:
        """
        return self.get_time_estimate() * self.cost_manager.get_cost_per_person_hour()


