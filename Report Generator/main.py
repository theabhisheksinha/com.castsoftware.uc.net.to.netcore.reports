from logger import Logger

from _version import __version__

from modules.module_register import ModuleRegister
from services.pre_process_service import PreProcessService
from utils.configuration.neo4j_connection_info import Neo4jConnectionConfiguration
from utils.configuration.working_directory_configuration import WorkingDirectoryConfiguration


def main():
    """
    Main function , initializing modules
    :return:
    """
    logger = Logger.get_logger("Net Migration Report. Version: {0}.".format(__version__))
    logger.info("Launching the Net Migration report. Version: {0}".format(__version__))

    try:
        # Modify global config
        logger.info("Setting working directory.")
        workdir_info = WorkingDirectoryConfiguration()
        workdir_info.verify()  # Get filepath  to save the file
        workdir = workdir_info.get_workdir()  # Get filepath  to save the file
        logger.info("Working directory is set to {0}.".format(workdir))
        # Verify working directory validity

        # Get Arguments
        logger.info("Retrieving Neo4j configuration.")
        neo4j_info = Neo4jConnectionConfiguration()
        application = neo4j_info.get_application()  # Get neo4j info, including app name
        logger.info("Now processing application '{0}'.".format(application))

        pre_pro = PreProcessService()
        pre_pro.launch()  # Launch pre processing actions on the KB

        module_registered = ModuleRegister()
        module_registered.launch_registered()
    except Exception as e:
        logger.error("Failed to launch the report generation.", e)
        print("Process failed")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
