import socket
import threading


from .util import Parser

# parse the incoming request (comes in as an RESP array)
# parse until the delimiter (which is /r/n - you also have to parse out the length of each
# element)
# once you've parsed the command, you can determine whether it's an echo or a ping
# if its an echo, you have to encode it in the same way (with an array response) (I think)

def handle_connection(incoming_connection):
    while True:
        try:
            command, *args = Parser(incoming_connection).decode()
            if command == b"ping":
                incoming_connection.send(b"+PONG\r\n")
            elif command == b"echo":
                pass
                # handle echo
            else:
                connection.send(b"-ERR Unknown Commmand Provided\r\n")
        except ConnectionError:
            print("Connection Error occurred")
            break


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        incoming_connection, _ = server_socket.accept()  # accept incoming connection
        thrd = threading.Thread(target=handle_connection, args=(incoming_connection,)) 
        thrd.start()


if __name__ == "__main__":
    main()
