import socket
import os
import json
from datetime import datetime

from variable import FILE_PATH, SERVER_ADDRESS

def run_socket_server(host = SERVER_ADDRESS['host'], port = SERVER_ADDRESS['port']):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    try:
        while True:
            print('Socket server is running......')
            data, address = server_socket.recvfrom(1024)
            if not data:
                break
            result = {}
            response = ''
            try:
                with open(os.path.join(*FILE_PATH['storage']),'rb') as f:
                    result = json.loads(f.read())
                with open(os.path.join(*FILE_PATH['storage']),'wb') as f:
                    value = json.loads(data.decode('utf-8'))
                    key = str(datetime.now())
                    result[key] = value
                    f.write(json.dumps(result).encode())
            except Exception as e:
                response = str(e)
            server_socket.sendto(response.encode(), address)
    except KeyboardInterrupt:
        server_socket.close()