

from dashboardWidgets.widgetConfig import WidgetConfig

class LineGauge(WidgetConfig):
    def __init__(self, xPos, yPos, nt4Topic_in, minRange, maxRange, minAcceptable, maxAcceptable):
        WidgetConfig.__init__(self, nt4Topic_in, xPos, yPos)
        self.nominalHeight = 5
        self.nominalWidth = 20
        self.minRange = minRange
        self.maxRange = maxRange
        self.minAcceptable = minAcceptable
        self.maxAcceptable = maxAcceptable
        self.isVisible = True

            
        
    def  getJSDeclaration(self):
        return f"var widget{self.idx} = new LineGauge('widget{self.idx}', '{self.name}',{self.minRange},{self.maxRange},{self.minAcceptable}, {self.maxAcceptable})\n"    

    def  getJSSetData(self):
        retStr = ""
        retStr += "if(name == \"" + self.nt4TopicCurVal + "\"){ "
        retStr += f"    widget{self.idx}.setVal(value)"
        retStr += "}"
        return retStr
    
    def  getJSUpdate(self) :
        return f"    widget{self.idx}.render()"
    
    def  getJSSetNoData(self):
        return f"    widget{self.idx}.reportNoData()"
    