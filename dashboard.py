from dashboardWidgets.autoChooser import AutoChooser
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text
import AutoSequencerV2.autoSequencer as AS


class Dashboard():
    def __init__(self, webserver):
        webserver.addDashboardWidget(
            Text(50, 75, "/SmartDashboard/faultDescription"))
        webserver.addDashboardWidget(
            SwerveState(85, 15))
        webserver.addDashboardWidget(
            AutoChooser(50, 10, AS.getInstance().getDelayModeNTTableName(), 
                        AS.getInstance().getDelayModeList()))
        webserver.addDashboardWidget(
            AutoChooser(50, 30, AS.getInstance().getMainModeNTTableName(), 
                        AS.getInstance().getMainModeList()))