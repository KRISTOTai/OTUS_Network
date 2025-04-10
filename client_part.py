import socket

HOST = '127.0.0.1'
PORT = 12345
STATUS = 404


def run_client():
    request = (
        f"GET /?status={STATUS} HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"User-Agent: TestClient/1.0\r\n"
        f"X-Custom-Header: EchoTest\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode('utf-8'))

        response = b''
        while True:
            part = s.recv(4096)
            if not part:
                break
            response += part

    print(response.decode('utf-8', errors='ignore'))


if __name__ == '__main__':
    run_client()
