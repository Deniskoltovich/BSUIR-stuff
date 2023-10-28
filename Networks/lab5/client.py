import socket
import argparse


def send_request(host, port, method, path, headers, body):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port)) # подкл к каналу

    try:
        # Create an HTTP request
        request = f"{method} {path} HTTP/1.1\r\n"
        request += "\r\n".join([f"{header}: {value}" for header, value in headers.items()])
        request += f"\r\n\r\n{body}\r\n"

        client_socket.send(request.encode())
        # GET localhost:8000 HTTP/1.1
        # "Content-Type: text/plain

        # {
        # "key":"val"
        # }
        #
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print(response.decode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def main():
    parser = argparse.ArgumentParser(description="Simple HTTP client")
    parser.add_argument("host", help="Target host")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("--path", help="HTTP request path", default='/')
    parser.add_argument("--method", default="GET", choices=["GET", "PUT", "OPTIONS"], help="HTTP method")
    parser.add_argument("--header", action="append", nargs=2, metavar=("key", "value"), help="Custom headers")
    parser.add_argument("--body", help="Request body")

    args = parser.parse_args()

    headers = {"Host": args.host}

    if args.header:
        headers.update(args.header)

    if args.method == "GET":
        args.body = ""

    send_request(args.host, args.port, args.method, args.path, headers, args.body)


if __name__ == "__main__":
    main()
