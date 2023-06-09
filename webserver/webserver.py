import socketserver
import socket
import threading
import functools

from webserver.templatingRequestHandler import TemplatingRequestHandler, dashboardWidgetList, WEB_ROOT

# A threaded TCP server starts up new python threads for each client request, which allows
# complex requests to be handled in the background and not bog down robot code
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# Main robot website server
class Webserver():
    
    def __init__(self):
        
        # Serve all contents of the webserver/www folder, with special
        # logic to handle filling out template html files
        handler = functools.partial(TemplatingRequestHandler, 
                                     directory=WEB_ROOT)

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
        
    # Ensure we invoke shutdown procedures on the class destruction
    def __del__(self):
        print("Server shutting down")
        self.shutdown()
            
    # Stop the server and the background thread its running in.
    def shutdown(self):
        self.server.shutdown()
        self.serverThread.join()
        
    # public api to submit a new dashboard widget
    def addDashboardWidget(self, widget):
        widget.idx = len(dashboardWidgetList)
        dashboardWidgetList.append(widget)