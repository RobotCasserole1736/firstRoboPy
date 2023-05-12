
# Base class for any dashboard widget and its configuration
class WidgetConfig:
    def __init__(self, nt4Topic_in):
        self.name = ""
        self.idx = 0
        self.nt4TopicCurVal = nt4Topic_in
        self.isVisible = False
        self.xPos = 0.0
        self.yPos = 0.0
        self.sizeScaleFactor = 1.0
        self.nominalWidth  = 0.0
        self.nominalHeight = 0.0

    def getTopicSubscriptionStrings(self):
        return "\"" + self.nt4TopicCurVal + "\","
    
    def getHTML(self):
        if(self.isVisible):
            height = self.nominalHeight * self.sizeScaleFactor
            width = self.nominalWidth * self.sizeScaleFactor
            retstr =  "<div class=\"widgetBase\" style=\"top:" + str(self.yPos-height/2) 
            retstr += "%;left:" + str(self.xPos-width/2) 
            retstr += "%;height:" + str(height) + "vw;width:" + str(width) 
            retstr += "vw\" id=\"widget" + str(self.idx) + "\"></div>"
            return retstr
        else:
            return ""

    def getJSDeclaration(self):
        return ""

    def getJSUpdate(self):
        return ""

    def getJSSetData(self):
        return ""

    def getJSSetNoData(self):
        return ""
    
    def getJSCallback(self):
        return ""
    
