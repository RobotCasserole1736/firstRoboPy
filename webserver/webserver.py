import http.server
import socketserver
import socket
import threading


class Webserver():
    
    def __init__(self):
        bgThread = threading.Thread(daemon=True, target=self.runServer)
        bgThread.start()

    def runServer(self):
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname)   
        PORT = 5805
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"Server started on {hostname} at {IPAddr}:{PORT}")
            httpd.serve_forever()
           
            
    def shutdown(self):
        pass