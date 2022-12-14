import socket
import json

from variable import SERVER_ADDRESS

def run_socket_client(host = SERVER_ADDRESS['host'], port = SERVER_ADDRESS['port'], data = ''):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = json.dumps(data).encode()
    client_socket.sendto(data, (host, port))
    response, address = client_socket.recvfrom(1024)
    client_socket.close()
    return response

