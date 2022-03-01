from repository.cleaning.cleaning_repository import CleaningRepository
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.logger import Logger


class PreProcessService(AbstractImagingService):
    """
    Pre processing of the Imaging database
    """

    def __init__(self, ):
        """
        Pre process
        """
        super(PreProcessService, self).__init__()
        self.__logger = Logger.get_logger("Pre Processor Service")
        self.__cleaning_repository = CleaningRepository(self.get_application_name())

    def launch(self):
        """
        Launch the pre processing service
        :return:
        """
        self.__cleaning_repository.clean_belongs_to()
