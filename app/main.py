import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    incoming_connection, _ = server_socket.accept()
    data = incoming_connection.recv(1024)

    for element in data:
        incoming_connection.send(b"+PONG\r\n")


if __name__ == "__main__":
    main()
