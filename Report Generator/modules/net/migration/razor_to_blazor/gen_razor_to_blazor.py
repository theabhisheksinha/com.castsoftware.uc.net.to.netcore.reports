import statistics
from typing import List

from neo4j.graph import Node

from logger import Logger
from maths.normalization.records_normalizer import RecordsNormalizer
from records.net.aspx_to_blazor_record import AspxToBlazorRecord
from reports.report_generator import ReportGenerator
from repository.artifacts.object_repository import ObjectRepository
from repository.artifacts.sub_object_repository import SubObjectRepository
from repository.net_metrics.razor_metrics_repository import RazorMetricsRepository
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.imaging.artifact_utils import ArtifactUtils

FILE_TITLE = "Razor_migration.csv"


class GenRazorToBlazor(AbstractImagingService):
    """
        Generate the Razor to Blazor migration plan
    """

    def __init__(self):
        super(GenRazorToBlazor, self).__init__()

        self.__logger = Logger.get_logger("Generator Razor to Blazor")
        self.__object_repository = ObjectRepository(self.get_application_name())
        self.__subobject_repository = SubObjectRepository(self.get_application_name())
        self.__razor_metrics_repository = RazorMetricsRepository(self.get_application_name())

    def create_record(self, node: Node) -> AspxToBlazorRecord:
        """
        Create the list of records
        :return:
        """
        record = AspxToBlazorRecord()

        record.aip_type = ArtifactUtils.get_type(node)
        record.name = ArtifactUtils.get_name(node)
        record.full_name = ArtifactUtils.get_fullname(node)
        record.html_loc = self.__object_repository.get_loc(node)

        # C# Class attached to it, and to migrate
        attached_cs_functions = []
        attached_cs_functions_fullname = []

        cs_loc = []
        cs_complexity = []

        for cs_node in self.__razor_metrics_repository.get_remote_function(node):
            attached_cs_functions.append(ArtifactUtils.get_name(cs_node))
            attached_cs_functions_fullname.append(ArtifactUtils.get_fullname(cs_node))
            cs_loc.append(self.__subobject_repository.get_loc(cs_node))
            cs_complexity.append(self.__subobject_repository.get_essential_complexity(cs_node))

        record.cs_average_loc_number = statistics.mean(cs_loc) if len(cs_loc) > 0 else 0
        record.cs_average_complexity = statistics.mean(cs_complexity) if len(cs_complexity) > 0 else 0

        record.cs_file_number = len(attached_cs_functions)
        record.cs_files_attached = attached_cs_functions_fullname[0] if len(
            attached_cs_functions_fullname) == 1 else attached_cs_functions_fullname

        return record

    def __get_records(self):
        """
        Get the list of records to treat
        :return:
        """
        # Get Node list on flagged method
        nodes = self.__object_repository.get_object_by_type("HTML5 CSHTML Content")

        records_list = []
        for x in nodes:
            try:
                records_list.append(self.create_record(x))
            except Exception as e:
                self.__logger.warn("*Failed to process node with id: {}".format(x.id))

        return RecordsNormalizer.normalize_records_difficulty(records_list)

    def generate(self) -> List:
        """
        Launch the report generation
        :return: List of record generated
        """
        records = self.__get_records()

        report = None
        try:
            report = ReportGenerator().set_path(self.get_working_dir()) \
                .set_file_name(FILE_TITLE).set_headers(AspxToBlazorRecord.get_headers()).build()

            for i, row in enumerate(records):
                report.write(row.get_record())

                if i % 100 == 0:
                    self.__logger.info(
                        "Exported {0} nodes on {1} at {2}.".format(i, len(records), report.get_file_name()))
        except Exception as e:
            self.__logger.error("Failed to generate the report.", e)
        finally:
            # Report close
            if report is not None:
                report.close()

        return records