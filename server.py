import socket
import threading
from _thread import *
from xml.etree import ElementTree


print_lock = threading.Lock()


def threaded_handler(connection, address):
    while True:
        data = connection.recv(1024)
        if not data or data == b'q':
            break

        print_lock.acquire()
        print('Received: {0} from {1}:{2}'.format(data, address[0], address[1]))
        connection.sendall(b'You sent \'%s\'' % data[::-1])
        print_lock.release()

    print('Connection closes')
    connection.close()


def server_main():
    config_xml = ElementTree.ElementTree(file='config.xml')
    host = config_xml.find('ip-address').text
    port = int(config_xml.find('port-number').text)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        print('Server listening on {0}:{1}'.format(host, port))
        while True:
            conn, addr = sock.accept()
            print('Connected to: {0}:{1}'.format(addr[0], addr[1]))
            start_new_thread(threaded_handler, (conn, addr))


if __name__ == '__main__':
    server_main()
