

import wpilib
from dashboardWidgets.widgetConfig import WidgetConfig


def getRIOStreamURL(port):
    if(wpilib.RobotBase.isSimulation()):
        return f"http://localhost:{port}"
    else:
        return f"http://roborio-1736-frc.local:{port}"

class Camera(WidgetConfig):
    def __init__(self, xPos, yPos, streamURL):
        WidgetConfig.__init__(self, "", xPos, yPos)
        self.nominalHeight = 30
        self.nominalWidth = 40
        self.isVisible = True
        self.streamURL = streamURL

    def  getJSDeclaration(self):
        return f"var widget{self.idx} = new Camera('widget{self.idx}', '{self.name}', '{self.streamURL}')\n"    
