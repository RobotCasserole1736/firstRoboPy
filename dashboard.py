from dashboardWidgets.autoChooser import AutoChooser
from dashboardWidgets.camera import Camera, getRIOStreamURL
from dashboardWidgets.circularGauge import CircularGauge
from dashboardWidgets.lineGauge import LineGauge
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text
import AutoSequencerV2.autoSequencer as AS


class Dashboard():
    def __init__(self, webserver):
        webserver.addDashboardWidget(
            CircularGauge(15, 15, "/SmartDashboard/test", -10,10,-5,5))
        webserver.addDashboardWidget(
            LineGauge(15, 50, "/SmartDashboard/test", -10,10,-5,5))
        webserver.addDashboardWidget(
            Text(30, 75, "/SmartDashboard/test"))
        webserver.addDashboardWidget(
            SwerveState(85, 15))
        webserver.addDashboardWidget(
            Camera(75, 60, getRIOStreamURL(1181)))
        webserver.addDashboardWidget(
            AutoChooser(50, 10, AS.getInstance().getDelayModeNTTableName(), 
                        AS.getInstance().getDelayModeList()))