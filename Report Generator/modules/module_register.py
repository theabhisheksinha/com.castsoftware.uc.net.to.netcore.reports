from modules.net.migration.net_migration_orchestrator import NetMigrationOrchestrator

class ModuleRegister:

    def __init__(self):
        """
        Initialize the Module register
        """
        self.migration_orchestrator = NetMigrationOrchestrator()

    def launch_registered(self):
        self.migration_orchestrator.launch()
