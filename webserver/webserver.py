import http.server
import socketserver
import socket
import threading
import functools

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



class Webserver():
    
    def __init__(self):
        
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, 
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