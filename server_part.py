import socket
import re
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

HOST = ''  # Пустая строка - слушаем на всех интерфейсах
PORT = 12345


# f"GET /?status={STATUS} HTTP/1.1\r\n"
# STATUS_PATTERN = re.compile(
#     r'(?P<status>.*?=)'
#     r'(?P<status_code>\d+)'
# )


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Echo server listening on port {PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                handle_request(conn, addr)


def handle_request(conn, addr):
    data = conn.recv(1024).decode('utf-8', errors='ignore')
    if not data:
        return

    lines = data.splitlines()
    request_line = lines[0]
    headers = lines[1:]

    parts = request_line.split()
    if len(parts) < 2:
        return

    method = parts[0]
    path = parts[1]
    status = parse_status_code(path)

    body = [
               f"Request Method: {method}",
               f"Request Source: {addr}",
               f"Response Status: {status.value} {status.phrase}",
           ] + headers

    response_body = "\r\n".join(body)
    response = (
        f"HTTP/1.1 {status.value} {status.phrase}\r\n"
        f"Content-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{response_body}"
    )

    conn.sendall(response.encode('utf-8'))


def parse_status_code(path):
    parsed_url = urlparse(path)
    query_params = parse_qs(parsed_url.query)

    try:
        code = int(query_params.get('status', [200])[
                       0])  # parse_qs превращает строку query в словарь, где значение представлено списком
        return HTTPStatus(code)
    except (ValueError, KeyError):
        return HTTPStatus(200)


if __name__ == '__main__':
    run_server()
