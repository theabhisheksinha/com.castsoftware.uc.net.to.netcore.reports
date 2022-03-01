from logger import Logger
from repository.AbstractRepository import AbstractRepository


class CleaningRepository(AbstractRepository):

    def __init__(self, application: str):
        """
            Initialize the NetMetrics service
            :param application: Application to process
       """
        super(CleaningRepository, self).__init__(application)

        self.__logger = Logger.get_logger("Cleaning repository")

    def clean_belongs_to(self) -> None:
        """
        Clean phantom links in the Imaging kb
        :return: The number of link removed
        """
        self.__logger.info("Cleaning old 'BELONGTO' links...")
        # Get the query to link an net object
        query = self.query_service.get_query("migration", "clean_links")
        query.replace_anchors({"APPLICATION": self.get_application()})

        # Execute
        res = self._neo4j_al.execute(query)
        val = res[0] if len(res) >= 1 else 0
        self.__logger.info("{0} old 'BELONGTO' links were removed.".format(val))
