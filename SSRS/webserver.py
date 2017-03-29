# -*- coding: utf-8 -*-

import socket
import sys

class http:
    
    def __init__(self, host='', port=8888):
        
        self.runserver(host, port)        
    
    def usage(self):
        msg = '''The following parameters are available:
            -> runserver'''
        print(msg)
        sys.exit(0)
    
    def runserver(self, HOST,PORT):
        '''
            Server implementation
        '''
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)
        print('Serving HTTP on port %s ...' % PORT)
        
        while True:
            
            try:
                client_connection, client_address = listen_socket.accept()
                request = client_connection.recv(1024)
                print(request)
                
                http_response = b"""Hello, World!"""
                client_connection.sendall(http_response)
                client_connection.close()
            
            except (KeyboardInterrupt, SystemExit):
                print('interrupted!')
                return
            

server = http()