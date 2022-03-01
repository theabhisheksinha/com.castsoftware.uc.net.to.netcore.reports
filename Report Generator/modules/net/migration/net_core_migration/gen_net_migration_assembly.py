from statistics import mean
from typing import List

from neo4j.graph import Node

from logger import Logger
from maths.normalization.records_normalizer import RecordsNormalizer
from records.net.assembly_decommission_record import AssemblyDecommissionRecord
from reports.report_generator import ReportGenerator
# META
from repository.artifacts.raw_repository import RawRepository
from repository.artifacts.sub_object_repository import SubObjectRepository
from repository.net_metrics.net_metrics_repository import NetMetricsRepository
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.imaging.artifact_utils import ArtifactUtils

FILE_TITLE = "Non_Compatible_Assembly_Class.csv"


class GenNetMigrationAssembly(AbstractImagingService):
    """
    Generate the effort report for the selected application in configuration

    """

    def create_record(self, node: Node) -> AssemblyDecommissionRecord:
        """
        Create the list of records
        :return:
        """
        record = AssemblyDecommissionRecord(node)

        # Default properties
        record.type = "Assembly"
        record.aip_type = ArtifactUtils.get_type(node)
        record.name = ArtifactUtils.get_name(node)
        record.full_name = ArtifactUtils.get_fullname(node)

        # Transaction in
        record.trans_in = self.__raw_object_service.get_transaction_in(node)

        record.compatible_net_core = self.__net_metrics.filter_compatibility_record(
            self.__raw_object_service.get_property_under(node, "Dotnet core"))

        record.compatible_standard_plus = self.__net_metrics.filter_compatibility_record(
            self.__raw_object_service.get_property_under(node, "Dotnet core plus platform extensions"))

        record.compatible_net_core_plus = self.__net_metrics.filter_compatibility_record(
            self.__raw_object_service.get_property_under(node, "Dotnet standard plus platform"))

        recommendation = set(self.__raw_object_service.get_property_under(node, "Dotnet migration recommended changes"))
        record.recommended_change = recommendation if len(recommendation) > 0 else ""

        cs_methods = []
        cs_loc_in = []
        cs_complexity_in = []

        # Parse attached cs methods
        for f in self.__raw_object_service.get_sub_object_caller_by_type(node):
            cs_methods.append(ArtifactUtils.get_fullname(f))
            cs_loc_in.append(self.__subobject_repository.get_loc(f))
            cs_complexity_in.append(self.__subobject_repository.get_essential_complexity(f))

        # CS Related
        record.cs_call_num = len(cs_methods)
        record.cs_methods_fullname = cs_methods
        record.cs_loc_in = sum(cs_loc_in) if len(cs_loc_in) > 0 else 0
        record.cs_complexity_in = mean(cs_complexity_in) if len(cs_complexity_in) > 0 else 0

        # Parent
        parent = self.__raw_object_service.get_parent(node)
        record.parent = ArtifactUtils.get_fullname(parent) if parent is not None else ""

        return record

    def __get_records(self):

        # Get Node list on flagged method
        nodes = self.__net_metrics.get_net_artifacts_object_like()

        # Get row
        records_list = []
        for x in nodes:
            try:
                records_list.append(self.create_record(x))
            except Exception as e:
                self.__logger.warn("Failed to process node with id: {}".format(x.id))

        return RecordsNormalizer.normalize_records_difficulty(records_list)

    def __init__(self):
        """
        Initialize the report service
        :param application: Application to process
        """
        super(GenNetMigrationAssembly, self).__init__()

        self.__logger = Logger.get_logger("Gen .Net Core Migration")
        self.__net_metrics = NetMetricsRepository(self.get_application_name())
        self.__raw_object_service = RawRepository(self.get_application_name())
        self.__subobject_repository = SubObjectRepository(self.get_application_name())

    def generate(self) -> List:
        """
        Launch the report generation
        :param file_path File Path
        :return:
        """

        # Get Node list on flagged method
        records = self.__get_records()


        report = None
        try:
            report = ReportGenerator().set_path(self.get_working_dir()) \
                .set_file_name(FILE_TITLE).set_headers(AssemblyDecommissionRecord.get_headers()).build()

            for i, rec in enumerate(records):
                report.write(rec.get_record())

                if i % 100 == 0:
                    self.__logger.info("Exported {0} nodes on {1} at {2}.".format(i, len(records),
                                                                                  report.get_file_name()))
        except Exception as e:
            self.__logger.error("Failed to generate the report.", e)
        finally:
            # Report close
            if report is not None:
                report.close()

        return records
