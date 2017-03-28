# -*- coding: utf-8 -*-

import socket
import sys

def usage():
    msg = '''The following parameters are available:
        -> runserver'''
    print(msg)
    sys.exit(0)

def runserver(HOST='',PORT=8888):
    '''
        Server implementation
    '''
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print('Serving HTTP on port %s ...' % PORT)
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)
        print(request)
    
        http_response = """\
    HTTP/1.1 200 OK
    
    Hello, World!
    """
        client_connection.sendall(http_response)
        client_connection.close()
        
        
args = sys.argv

# No parameter specified
if len(args) == 1:
    usage()

# Check for runserver param    
if 'runserver' in args:
    p_index = args.index('runserver', )
    
    # Check if Host, Port was informed
    if p_index < len(args):
        
        # check if the informed host and port is a tuple
        if isinstance(args[p_index], tuple):
            runserver(args[p_index])
        
        else:
            raise BaseException("Specify the host and port as a tuple")
    
    else:
        
        runserver()