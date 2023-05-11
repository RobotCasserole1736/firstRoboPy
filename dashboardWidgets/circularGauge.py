

from dashboardWidgets.widgetConfig import WidgetConfig

class CircularGauge(WidgetConfig):
    def __init__(self, nt4Topic_in, minRange, maxRange, minAcceptable, maxAcceptable):
        WidgetConfig.__init__(self, nt4Topic_in)
        self.nominalHeight = 20
        self.nominalWidth = 20
        self.minRange = minRange
        self.maxRange = maxRange
        self.minAcceptable = minAcceptable
        self.maxAcceptable = maxAcceptable
        self.isVisible = True
            
        
    def  getJSDeclaration(self):
        return "var widget{self.idx} = new CircularGauge('widget{self.idx}', '{self.name}',{self.minRange},{self.maxRange},{self.minAcceptable}, {self.maxAcceptable})\n"    
    
    def  getJSSetData(self):
        retStr = ""
        retStr += "if(name == \"" + self.nt4TopicCurVal + "\"): "
        retStr += "    widget{self.idx}.setVal(value)"
        retStr += ""
        return retStr
    
    def  getJSUpdate(self) :
        return "    widget{self.idx}.render()"
    
    def  getJSSetNoData(self):
        return "    widget{self.idx}.reportNoData()"
    