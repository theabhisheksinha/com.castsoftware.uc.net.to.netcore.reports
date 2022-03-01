from typing import List

from neo4j.graph import Node

from logger import Logger
from maths.normalization.records_normalizer import RecordsNormalizer
from records.net.apx_migration_record import AspxMigrationRecord
from reports.report_generator import ReportGenerator
from repository.artifacts.object_repository import ObjectRepository
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.imaging.artifact_utils import ArtifactUtils

FILE_TITLE = "Aspx_migration.csv"


class GenASPXPlan(AbstractImagingService):
    """
        Generate ASPX migration plan
    """

    def __init__(self):
        super(GenASPXPlan, self).__init__()

        self.__logger = Logger.get_logger("Generator Aspx Migration")
        self.__object_repository = ObjectRepository(self.get_application_name())

    def create_record(self, node: Node) -> AspxMigrationRecord:
        """
        Create the list of records
        :return:
        """
        record = AspxMigrationRecord(node)

        record.aip_type = ArtifactUtils.get_type(node)
        record.name = ArtifactUtils.get_name(node)
        record.full_name = ArtifactUtils.get_fullname(node)
        record.html_loc = self.__object_repository.get_loc(node)

        # C# Class attached to it, and to migrate
        attached_files = []
        attached_files_fullname = []

        for cs_node in self.__object_repository.get_callees_by_type(node, "C# Class"):
            attached_files.append(ArtifactUtils.get_name(cs_node))
            attached_files_fullname.append(ArtifactUtils.get_fullname(cs_node))
            record.cs_loc += self.__object_repository.get_loc(cs_node)
            record.cs_complexity += self.__object_repository.get_inner_essential_complexity(cs_node)

        record.attached_cs_file = attached_files[0] if len(attached_files) == 1 else attached_files
        record.attached_cs_fullname = attached_files_fullname[0] if len(
            attached_files_fullname) == 1 else attached_files_fullname

        return record

    def __get_records(self):

        # Get Node list on flagged method
        nodes = self.__object_repository.get_object_by_type("Active Server PageX")

        # Get row
        records_list = []
        for x in nodes:
            try:
                records_list.append(self.create_record(x))
            except Exception as e:
                self.__logger.warn("Failed to process node with id: {}".format(x.id))

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
                .set_file_name(FILE_TITLE).set_headers(AspxMigrationRecord.get_headers()).build()

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
