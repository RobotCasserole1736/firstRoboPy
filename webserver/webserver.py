import http.server
import socketserver
import socket
import threading
import functools

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



class Webserver():
    
    def __init__(self):
        
        Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="webserver/www/")

        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname)   
        PORT = 5805

        self.server = ThreadedTCPServer(("", PORT), Handler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"Server started on {hostname} at {IPAddr}:{PORT} in thread { self.server_thread.name}")
        
    def __del__(self):
        print("Server shutting down")
        self.shutdown()
            
    def shutdown(self):
        self.server.shutdown()
        self.server_thread.join()