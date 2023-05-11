from http.server import SimpleHTTPRequestHandler
import socketserver
import socket
import threading
import functools

_dashboardWidgetList = []

htmlTmpltTxt = ""
with open("webserver/www/dashboard/dashboard.html_tmplt", "r") as infile:
    htmlTmpltTxt = infile.read()
    
jsTmpltTxt = ""
with open("webserver/www/dashboard/dashboard.js_tmplt", "r") as infile:
    jsTmpltTxt = infile.read()

class TemplatingRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):

        if self.path == "/dashboard/dashboard.html":

            retText = ""

            repTxt = ""
            for widget in _dashboardWidgetList:
                repTxt += widget.getHTML()
                repTxt += "\n"
                
            retText = htmlTmpltTxt.replace("${WIDGETS_HTML}", repTxt)
                     
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()                

            self.wfile.write(retText.encode())

            return SimpleHTTPRequestHandler
        
        elif self.path == "/dashboard/dashboard.js":

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write("hello this is also dog".encode())

            return SimpleHTTPRequestHandler
        
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
        


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Webserver():
    
    def __init__(self):
        
        handler = functools.partial(TemplatingRequestHandler, 
                                     directory="webserver/www/")

        hostname=socket.gethostname()   
        ipAddr=socket.gethostbyname(hostname)   
        port = 5805

        self.server = ThreadedTCPServer(("", port), handler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        self.serverThread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        self.serverThread.daemon = True
        self.serverThread.start()
        print(f"Server started on {hostname} at {ipAddr}:{port} " + 
              "in thread { self.serverThread.name}")
        
    def __del__(self):
        print("Server shutting down")
        self.shutdown()
            
    def shutdown(self):
        self.server.shutdown()
        self.serverThread.join()
        
    def addDashboardWidget(self, widget):
        _dashboardWidgetList.append(widget)