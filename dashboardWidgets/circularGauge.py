

from dashboardWidgets.widgetConfig import WidgetConfig

class CircularGauge(WidgetConfig):
    def __init__(self, xPos, yPos, nt4Topic_in, minRange, maxRange, minAcceptable, maxAcceptable):
        WidgetConfig.__init__(self, nt4Topic_in)
        self.nominalHeight = 20
        self.nominalWidth = 20
        self.minRange = minRange
        self.maxRange = maxRange
        self.minAcceptable = minAcceptable
        self.maxAcceptable = maxAcceptable
        self.isVisible = True
        self.xPos = xPos
        self.yPos = yPos
            
        
    def  getJSDeclaration(self):
        return f"var widget{self.idx} = new CircularGauge('widget{self.idx}', '{self.name}',{self.minRange},{self.maxRange},{self.minAcceptable}, {self.maxAcceptable})\n"    
    
    def  getJSSetData(self):
        retStr = ""
        retStr += f"if(name == \"" + self.nt4TopicCurVal + "\"){ "
        retStr += f"    widget{self.idx}.setVal(value)"
        retStr += "}"
        return retStr
    
    def  getJSUpdate(self) :
        return f"    widget{self.idx}.render()"
    
    def  getJSSetNoData(self):
        return f"    widget{self.idx}.reportNoData()"
    