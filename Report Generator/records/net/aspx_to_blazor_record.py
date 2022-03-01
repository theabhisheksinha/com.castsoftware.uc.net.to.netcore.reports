from records.abstract_migration_record import AbstractMigrationRecord


class AspxToBlazorRecord(AbstractMigrationRecord):
    """
    ASpx Conversion to Blazor page
    """

    def get_difficulty_score(self):
        self.difficulty_score = self.html_loc + (
                    self.cs_average_complexity * self.cs_average_loc_number) * self.cs_file_number
        return self.difficulty_score

    def get_time_estimate(self):
        """
        Get Time estimate
        :return:
        """
        cs_loc_cost = float(self.time_manager.get_time_factor("CSHARP", "rewrite", "loc"))
        html_loc_cost = float(self.time_manager.get_time_factor("HTML", "rewrite", "loc"))

        cs_cost = self.cs_average_loc_number * self.cs_file_number * cs_loc_cost
        html_cost = self.html_loc * html_loc_cost

        return self.get_normalized_score() * cs_cost + html_cost

    def get_cost_estimate(self):
        return self.get_time_estimate() * self.cost_manager.get_cost_per_person_hour()

    def get_record(self):
        """
        Get record value
        :return:
        """
        return [
            self.aip_type,
            self.name,
            self.full_name,
            self.html_loc,

            self.cs_file_number,
            self.cs_files_attached,
            self.cs_average_loc_number,
            self.cs_average_complexity,

            self.get_normalized_score(),
            self.get_difficulty_segment(),
            self.get_time_estimate(),
            self.get_cost_estimate()
        ]

    @staticmethod
    def get_headers():
        return [
            "Object Type",
            "Name",
            "Full Name",
            "HTML Loc",
            "CS File Number",
            "CS Files attached",
            "CS Average LOC",
            "CS Average Complexity",
            "Difficulty Normalized",
            "Difficulty Segment",
            "Time Estimate",
            "Cost Estimate"
        ]

    def __init__(self):
        """
        ASPX to Blazor
        """

        super().__init__()
        self.aip_type = ""
        self.name = ""
        self.full_name = ""

        self.cs_files_attached = []
        self.cs_file_number = 0
        self.cs_average_loc_number = 0
        self.cs_average_complexity = 0

        self.html_loc = 0
        self.difficulty_segment = 0
