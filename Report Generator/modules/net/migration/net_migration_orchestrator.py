from modules.net.migration.aspx_migration.gen_aspx_plan import GenASPXPlan
from modules.net.migration.net_core_migration.gen_action_plan import GenActionPlan
from modules.net.migration.net_core_migration.gen_net_migration_assembly import GenNetMigrationAssembly
from modules.net.migration.net_core_migration.gen_net_migration_raw import GenNetMigrationRaw
from modules.net.migration.razor_to_blazor.gen_razor_to_blazor import GenRazorToBlazor


class NetMigrationOrchestrator:
    """
    Orchestrator
    """

    def __init__(self):
        pass

    def launch(self):
        """
        Launch the .Net File Migration
        :return:
        """
        # ASPX : Rewrite difficulty
        apx_migration = GenASPXPlan().generate()
        razor_migration = GenRazorToBlazor().generate()

        # Net Core Migration
        net_record = GenNetMigrationRaw().generate()
        net_raw_record = GenNetMigrationAssembly().generate()
        action_plan = GenActionPlan(net_raw_record).generate()
