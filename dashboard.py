from dashboardWidgets.autoChooser import AutoChooser
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text


class Dashboard():
    def __init__(self, webserver, autosequencer):
        webserver.addDashboardWidget(
            Text(50, 75, "/SmartDashboard/faultDescription"))
        webserver.addDashboardWidget(
            SwerveState(85, 15))
        webserver.addDashboardWidget(
            AutoChooser(50, 10, autosequencer.getDelayModeNTTableName(), 
                        autosequencer.getDelayModeList()))
        webserver.addDashboardWidget(
            AutoChooser(50, 20, autosequencer.getMainModeNTTableName(), 
                        autosequencer.getMainModeList()))