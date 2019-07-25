import socket
from xml.etree import ElementTree


config_xml = ElementTree.ElementTree(file='config.xml')

HOST = config_xml.find('ip-address').text
PORT = int(config_xml.find('port-number').text)

server_addr = (HOST, PORT)


def client_main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print('Connected to {}'.format(server_addr))
        while True:
            message = input('Enter message: ')
            s.sendall(message.encode('ascii'))
            data = s.recv(1024)
            print('Received: {}'.format(data.decode('ascii')))


if __name__ == '__main__':
    client_main()
