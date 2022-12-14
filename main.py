from threading import Thread

from services import run_server, run_socket_server
from variable import FILE_PATH, SERVER_ADDRESS


if __name__ == '__main__':
    thread_http = Thread(target=run_server, args=(SERVER_ADDRESS['host'], SERVER_ADDRESS['port']))
    thread_socket = Thread(target=run_socket_server, args=(SERVER_ADDRESS['host'], SERVER_ADDRESS['port']))
    thread_http.start()
    thread_socket.start()
