import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, _ = server_socket.accept()
        with conn:
            data = conn.recv(1024).split(b"\r\n")
            requestInfo = data[0].split(b" ")
            requestMethod = requestInfo[0].decode()
            requestSegments = requestInfo[1].decode().split("/")

            print("Method:", requestMethod)
            print("Segments:", requestSegments)

            match requestSegments[1]:
                case "":
                    conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
                case "echo":
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(requestSegments[2])}\r\n\r\n{requestSegments[2]}"
                    conn.sendall(response.encode())
                case _:
                    conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

            print(data)


if __name__ == "__main__":
    main()
