from dashboardWidgets.widgetConfig import WidgetConfig
from utils.signalLogging import sigNameToNT4TopicName

# Describes a set of topics associated with one module
class SwerveStateTopicSet:

     def __init__(self, modName, modIdx_in):
        self.azmthDesTopic = sigNameToNT4TopicName(f"DtModule_{modName}_azmthDes")
        self.azmthActTopic = sigNameToNT4TopicName(f"DtModule_{modName}_azmthAct")
        self.speedDesTopic = sigNameToNT4TopicName(f"DtModule_{modName}_speedDes")
        self.speedActTopic = sigNameToNT4TopicName(f"DtModule_{modName}_speedAct")
        self.modIdx = modIdx_in
    

     def getSubscriptionStrings(self):
        retStr = ""
        retStr += f"\"{self.azmthDesTopic}\","
        retStr += f"\"{self.azmthActTopic}\","
        retStr += f"\"{self.speedDesTopic}\","
        retStr += f"\"{self.speedActTopic}\","
        return retStr

     def getJSSetData(self, widgetIdx):
        retStr = ""
        retStr += f"if(name == \"{self.azmthDesTopic}\") {{\n"
        retStr += f"    widget{widgetIdx}.setVal({self.modIdx}, 0, value)\n"
        retStr += f"}}\n"
        retStr += f"if(name == \"{self.azmthActTopic}\") {{\n"
        retStr += f"    widget{widgetIdx}.setVal({self.modIdx}, 1, value)\n"
        retStr += f"}}\n"
        retStr += f"if(name == \"{self.speedDesTopic}\") {{\n"
        retStr += f"    widget{widgetIdx}.setVal({self.modIdx}, 2, value)\n"
        retStr += f"}}\n"
        retStr += f"if(name == \"{self.speedActTopic}\") {{\n"
        retStr += f"    widget{widgetIdx}.setVal({self.modIdx}, 3, value)\n"
        retStr += f"}}\n"
        return retStr


class SwerveStateConfig(WidgetConfig):

    def __init__(self, xPos, yPos):
        WidgetConfig.__init__(self, None, xPos, yPos)
        self.nominalHeight = 30
        self.nominalWidth = 30
        self.FLTopics = SwerveStateTopicSet("FL", 0)
        self.FRTopics = SwerveStateTopicSet("FR", 1)
        self.BLTopics = SwerveStateTopicSet("BL", 2)
        self.BRTopics = SwerveStateTopicSet("BR", 3)


    def  getJSDeclaration(self):
        return f"var widget{self.idx} = new SwerveState('widget{self.idx}', '{self.name}')\n"    
    
    def getTopicSubscriptionStrings(self):
        retStr = ""
        retStr += self.FLTopics.getSubscriptionStrings()
        retStr += self.FRTopics.getSubscriptionStrings()
        retStr += self.BLTopics.getSubscriptionStrings()
        retStr += self.BRTopics.getSubscriptionStrings()
        return retStr;    

    def  getJSSetData(self):
        retStr = ""
        retStr += self.FLTopics.getJSSetData(0)
        retStr += self.FRTopics.getJSSetData(1)
        retStr += self.BLTopics.getJSSetData(2)
        retStr += self.BRTopics.getJSSetData(3)
        return retStr
    
    def  getJSUpdate(self) :
        return f"    widget{self.idx}.render()"
    
