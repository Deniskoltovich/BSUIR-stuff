import argparse
import json
import socket
import os


def handle(request):
    method = request.split(' ')[0]
    try:
        if method == 'GET':
            print(request)
            path = request.split('/?')[1]
            path = path.split('=')[1].split(' ')[0]
        elif method == 'PUT':
            body_start = request.index('{')
            body_end = request.index('}')
            content = request[body_start: body_end + 1]
            content = json.loads(content)
            print('content:\n\n', content, end='\n\n\n')
            path = content.pop('file')
        else:
            return handle_options()
        print('file: ', path)
        if os.path.isfile(path):
            if method == 'GET':
                return handle_get(path)
            elif method == 'PUT':
                return handle_put(path, content)
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\nFile not found'
            return response.encode('utf-8')

    except Exception as e:
        print(f'Error handling {method} request: {str(e)}')
        return b'HTTP/1.1 500 Internal Server Error\r\n\r\nAn error occurred'


def handle_get(path: str):
    with open(path, 'rb') as file:
        content = file.read()
    response = 'HTTP/1.1 200 OK\r\n'
    response += f'Content-Type: application/{path.split(".")[-1]}\r\n'
    response += 'Content-Length: ' + str(len(content)) + '\r\n'
    response += '\r\n'  # Пустая строка между заголовками и телом
    response = response.encode('utf-8') + content

    return response


def handle_put(path: str, content):
    lines = [line + '\n' for line in content.values()]
    with open(path, 'a') as file:
        file.writelines(lines)

    # Construct the response
    response_body = "Data saved successfully."

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/plain\r\n"
    response += "Content-Length: " + str(len(response_body)) + "\r\n"
    response += "\r\n"  # Blank line between headers and body
    response += response_body

    return response.encode('utf-8')

def handle_options():
    response = "HTTP/1.1 200 OK\r\n" + \
                'Allow: GET, POST, OPTIONS\r\n' + \
               'Access-Control-Allow-Origin: *\r\n' + \
               'Access-Control-Allow-Methods: GET, PUT, OPTIONS\r\n' + \
               'Access-Control-Allow-Headers: Content-Type\r\n\r\n'

    return response.encode('utf-8')


def main():
    # Create an ArgumentParser to handle command-line arguments
    parser = argparse.ArgumentParser(description="Simple HTTP server")
    parser.add_argument("--port", type=int, default=8001, help="Port to listen on")
    args = parser.parse_args()

    host = '127.0.0.1'
    port = args.port

    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')

        if data:
            response = handle(data)
            client_socket.send(response)

        client_socket.close()

if __name__ == "__main__":
    main()

