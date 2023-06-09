
from http.server import SimpleHTTPRequestHandler
import os
import platform
import sys, pathlib
import wpilib

# Global list of all widgets on the dashboard. 
dashboardWidgetList = []

# Where we expect to find our template files at 
WEB_ROOT = pathlib.Path(__file__).parent / "www"
DASHBOARD_ROOT = WEB_ROOT / "dashboard"

# One-time, read in all the template files we'll fill out
INDEX_TMPLT_TXT = ""
with open(WEB_ROOT / "index.html_tmplt", "r", encoding="utf-8") as infile: 
    INDEX_TMPLT_TXT = infile.read()
    
HTML_TMPLT_TXT = ""
with open(DASHBOARD_ROOT / "dashboard.html_tmplt", "r", encoding="utf-8") as infile:
    HTML_TMPLT_TXT = infile.read()
    
JS_TMPLT_TXT = ""
with open(DASHBOARD_ROOT / "dashboard.js_tmplt", "r", encoding="utf-8") as infile:
    JS_TMPLT_TXT = infile.read()

# A TemplatingRequestsHandler responds to web queries just like
# python's built in SimpleHTTPRequestsHandler, with additional
# hooks for special files that need to be filled out from templates
class TemplatingRequestHandler(SimpleHTTPRequestHandler):
    # This code-generation class has some long lines 
    # that I don't know of a good way to get rid of.
    # pylint: disable=line-too-long
    
    # from https://gist.github.com/HaiyangXu/ec88cbdce3cdbac7b8d5
    # Chrome barfs at you about "wrong response type" without this
    extensions_map = {
        '': 'application/octet-stream',
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg':	'image/svg+xml',
        '.css':	'text/css',
        '.js':'application/x-javascript',
        '.wasm': 'application/wasm',
        '.json': 'application/json',
        '.xml': 'application/xml',
    }
    
    # Fill out and return the index HTML page
    # This is the main landing page of the robot and includes robopy-provided
    # deploy information
    def handleIndexPage(self):
        if wpilib.RobotBase.isSimulation() :
            deployText = "Simulation \n"
        else:
            data = wpilib.deployinfo.getDeployData()
            deployText =  f"Deployed From: { data['deploy-host'] } \n"
            deployText +=  f"Deployed By: { data['deploy-user'] } \n"
            deployText +=  f"Deployed On: { data['deploy-date'] } \n"
            deployText +=  f"Source Project: { data['code-path'] } \n"
            deployText +=  f"Git Commit: { data['git-desc'] } \n"
            deployText +=  f"Git Branch: { data['git-branch'] } \n"
            deployText += f"RIO FPGA Sw: v{wpilib.RobotController.getFPGAVersion()} r{wpilib.RobotController.getFPGARevision()} \n"
            deployText += f"RIO Serial Number:{wpilib.RobotController.getSerialNumber()} \n"
            deployText += f"{wpilib.RobotController.getComments()} \n"
            
        deployText += f"Python {platform.python_version()} - {sys.executable} \n"
        deployText += f"Working Dir: {os.getcwd()}\n"


        filledOut = INDEX_TMPLT_TXT.replace("${BUILD_INFO}", deployText)
                    
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()                

        self.wfile.write(filledOut.encode())

        return SimpleHTTPRequestHandler
    
    # Fill out and return the HTML page for the dashboard
    def handleDashboardHtml(self):
        filledOut = ""

        htmlText = ""
        for widget in dashboardWidgetList:
            htmlText += widget.getHTML()
            htmlText += "\n"
            
        filledOut = HTML_TMPLT_TXT.replace("${WIDGETS_HTML}", htmlText)
                    
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()                

        self.wfile.write(filledOut.encode())

        return SimpleHTTPRequestHandler
    
    # Fill out and return the javascript page for the dashboard
    def handleDashboardJs(self):
        jsInstantiate = ""
        jsUpdate = ""
        jsCallback = ""
        jsSetData = ""
        jsSetNoData = ""
        subscribeLine = "nt4Client.subscribePeriodic(["

        for widget in dashboardWidgetList:
            jsInstantiate += widget.getJSDeclaration()
            jsInstantiate += "\n"

            jsUpdate += widget.getJSUpdate()
            jsUpdate += "\n"

            jsSetData += widget.getJSSetData()
            jsSetData += "\n"

            jsSetNoData += widget.getJSSetNoData()
            jsSetNoData += "\n"

            jsCallback += widget.getJSCallback()
            jsCallback += "\n"

            subscribeLine +=  widget.getTopicSubscriptionStrings()

        # Remove the trailing comma and close out the line
        subscribeLine = subscribeLine[:-1]
        subscribeLine += "], 0.05);" # 50ms sample rate
        subscribeLine += "\n"

        filledOut = JS_TMPLT_TXT
        filledOut = filledOut.replace("${WIDGETS_INSTANTIATE}", jsInstantiate)
        filledOut = filledOut.replace("${WIDGETS_NT4_SUBSCRIBE}", subscribeLine)
        filledOut = filledOut.replace("${WIDGETS_UPDATE}", jsUpdate)
        filledOut = filledOut.replace("${WIDGETS_SET_VALUE}", jsSetData)
        filledOut = filledOut.replace("${WIDGETS_SET_NO_DATA}", jsSetNoData)
        filledOut = filledOut.replace("${WIDGETS_CALLBACK}", jsCallback)

        self.send_response(200)
        self.send_header("Content-Type", "application/x-javascript")
        self.end_headers()

        self.wfile.write(filledOut.encode())

        return SimpleHTTPRequestHandler

    # Override the get method to apply templates on the files which need templating
    def do_GET(self):
        # Check for known tempaltes first
        if self.path in ("/index.html", "/") :
            return self.handleIndexPage()
        elif self.path == "/dashboard/dashboard.html":
            return self.handleDashboardHtml()
        elif self.path == "/dashboard/dashboard.js":
            return self.handleDashboardJs()
        else:
            # Fallback on serving like a normal HTTP request handler
            return SimpleHTTPRequestHandler.do_GET(self)
        