# coding=utf-8
import socket


EOL1 = b'\n\n'
EOL2 = b'\n\r\n'


def handle_connection(conn, addr):
    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
        print('handle_connection request :', request)
    conn.send(b'hello')

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 9999))
    serversocket.listen(5)
    print('http://127.0.0.1:9999')

    try:
        while True:
            conn, address = serversocket.accept()
            import pdb;pdb.set_trace()
            # print('conn:', conn,
            #       '\naddress :', address)
            handle_connection(conn, address)
    finally:
        serversocket.close()

if __name__ == '__main__':
    main()