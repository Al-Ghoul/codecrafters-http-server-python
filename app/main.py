import socket
from threading import Thread

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, _ = server_socket.accept()
        t = Thread(target=handle_connection, args=(conn,))
        t.start()


def handle_connection(conn: socket.socket):
    with conn:
        data = conn.recv(1024)
        requestData = data.split(b"\r\n")
        requestInfo = requestData[0].split(b" ")
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
            case "user-agent":
                userAgent = (
                    data[data.find(b"User-Agent") :].split(b" ")[1].strip(b"\r\n")
                )
                print(userAgent)
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(userAgent)}\r\n\r\n{userAgent.decode()}"
                conn.sendall(response.encode())
            case _:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
