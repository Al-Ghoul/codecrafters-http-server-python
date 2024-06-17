import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, _ = server_socket.accept()
        with conn:
            data = conn.recv(1024).split(b"\r\n")
            requestInfo = data[0].split(b" ")
            requestMethod = requestInfo[0].decode()
            requestPath = requestInfo[1].decode()

            print("Method:", requestMethod)
            print("Path:", requestPath)

            match requestPath:
                case "/":
                    conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
                case _:
                    conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

            print(data)


if __name__ == "__main__":
    main()
