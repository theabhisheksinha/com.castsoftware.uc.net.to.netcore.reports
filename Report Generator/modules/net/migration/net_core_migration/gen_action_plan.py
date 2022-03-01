from typing import List

from enums.artifact_type import ArtifactType
from enums.complexity_type import ComplexityType
from records.net.action_plan_record import ActionPlanRecord
from records.net.assembly_decommission_record import AssemblyDecommissionRecord
from reports.report_generator import ReportGenerator
from repository.artifacts.artifacts_repository import ArtifactRepository
from repository.net_metrics.net_metrics_repository import NetMetricsRepository
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.imaging.artifact_utils import ArtifactUtils
from utils.logger import Logger

# META
FILE_TITLE = "Action_plan.csv"


class GenActionPlan(AbstractImagingService):
    """
    Pre processing of the Imaging database
    """

    def __init__(self, net_migration_records: List):
        super(GenActionPlan, self).__init__()

        self.__logger = Logger.get_logger("Generator Action Plan")

        # Artifacts
        self.__object_repository = ArtifactRepository(self.get_application_name(), ArtifactType.OBJECT)
        self.__sub_object_repository = ArtifactRepository(self.get_application_name(), ArtifactType.SUB_OBJECT)
        self.__raw_object_repository = ArtifactRepository(self.get_application_name(), ArtifactType.RAW)

        self.__net_migration_repository = NetMetricsRepository(self.get_application_name())

        self.__net_migration_records = net_migration_records

    def create_records(self, record: AssemblyDecommissionRecord) -> List[ActionPlanRecord]:
        """
        Create a new action plan records
        :param record: Report records used to generate the action plan records
        :return:
        """
        ret_list = []

        if record.node is None:
            return ret_list

        # Get Type
        # Get Sub Objects linked to the records
        sub_objects = self.__net_migration_repository.get_sub_object_list(record.node)
        for node in sub_objects:

            main_label = ArtifactUtils.get_label(node, self.get_application_name())
            artifact_type = ArtifactType.from_type(main_label)

            # Get service type
            if artifact_type == ArtifactType.OBJECT:
                service = self.__object_repository
            elif artifact_type == ArtifactType.SUB_OBJECT:
                service = self.__sub_object_repository
            else:
                service = self.__raw_object_repository

            apr = ActionPlanRecord(node)

            apr.aip_type = artifact_type
            apr.name = ArtifactUtils.get_name(node)
            apr.full_name = ArtifactUtils.get_fullname(node)
            apr.aip_type = artifact_type.name[0]

            apr.net_core_fullname = record.name
            apr.net_core_class = record.parent

            parent = service.get_parent(node)
            apr.parent_class = ArtifactUtils.get_fullname(parent) if parent is not None else ""

            apr.compatible_standard_plus = record.compatible_standard_plus
            apr.compatible_net_core_plus = record.compatible_net_core_plus
            apr.compatible_net_core = record.compatible_net_core

            apr.essential_complexity = service.get_complexity(node, ComplexityType.ESSENTIAL)

            apr.trans_in = service.get_transaction_number(node) + 1

            ret_list.append(apr)
        # Calculate Complexity on other objects

        return ret_list

    def generate(self):
        """
            Generate the plan based on the detection of the previous records
            :return:
        """
        # Get Node list on flagged method
        methods_list = []  # Methods from the code to handle
        for rec in self.__net_migration_records:
            report_records = self.create_records(rec)
            methods_list.extend(report_records)

        # Filter the list
        methods_list.sort(key=lambda x: x.name, reverse=True)
        methods_list = set(methods_list)

        report = None
        try:
            report = ReportGenerator().set_path(self.get_working_dir()) \
                .set_file_name(FILE_TITLE).set_headers(ActionPlanRecord.get_headers()).build()

            for i, rec in enumerate(methods_list):
                if i % 100 == 0:
                    self.__logger.info("Exported {0} nodes on {1} at {2}.".format(i, len(methods_list),
                                                                                  report.get_file_name()))
                report.write(rec.get_record())  # Write row
        except Exception as e:
            self.__logger.error("Failed to generate the report.", e)
        finally:
            # Report close
            if report is not None:
                report.close()
