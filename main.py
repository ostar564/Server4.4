# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os
import codecs
# constants
IP = '127.0.0.1'
PORT = 8080
SOCKET_TIMEOUT = 10
REDIRECTION_DICTIONARY = {'index1.html': 'index.html'}


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    filename = "C:\\Users\\User\\Documents\\עומר סייבר\\סייבר"
    split_recourse = resource.split("\\")
    for split in split_recourse[1:]:
        filename += '\\' + split
# TO DO: check if URL had been redirected, not available or other error code. For example:
    name = filename[len(filename) - filename[::-1].index("\\"):len(filename)]
    if os.path.isfile(filename):
        data = get_file_data(filename)
        http_header = "HTTP/1.1 200\r\n"
        http_header += f"Content-Length: {(os.path.getsize(filename))}\r\n"
        http_header += f"Content-Type: {content_type(filename)}\r\n"
        http_header += "\r\n"
        http_response = http_header.encode('UTF-8')
        if isinstance(data, bytes):
            http_response += data
        else:
            http_response += data.encode('UTF-8')
        client_socket.send(http_response)
    elif name in REDIRECTION_DICTIONARY.keys():
        header_302 = "HTTP/1.1 302\r\n" + "Location:" + filename[len(filename): len(filename) - filename[::-1].index("\\")] + REDIRECTION_DICTIONARY[name] + "\r\n\r\n"
        print(header_302)
        header_302 = header_302.encode('UTF-8')
        client_socket.send(header_302)
    else:
        header_404 = "HTTP/1.1 404 \r\n\r\n".encode()
        client_socket.send(header_404)


def get_file_data(filename):
    """
    :param filename:
    :return: Gets file path and returns it's content
    """
    file = codecs.open(filename, "rb")#might be rb
    str1 = file.read()
    file.close()
    return str1


def content_type(filename):
    """
    :param filename:
    :return: type of file
    """
    name = filename[len(filename) - filename[::-1].index("."):len(filename)]
    if name == "html" or name == "txt":
        return "text/html; charset=utf-8"
    if name == "jpg" or name == "ico" or name == "gif" or name == "png" or name:
        return 'image/jpeg'
    if name == "css":
        return 'text/css'
    if name == "js":
        return "text/javascript; charset=UTF-8"


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    request_str = request.decode('utf-8')
    print(request_str)
    split_request = request_str.split(' ')
    if (split_request[0] == 'GET') and split_request[2].startswith('HTTP/1.1'):
            request_url = split_request[1].replace("/", "\\")
            x = (True, request_url)
            return x
    y = (False, None)
    return y


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        # get client request
        client_request = client_socket.recv(4096)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
        else:
            print('Error: Not a valid HTTP request')
            header_500 = "HTTP/1.1 500 \r\n\r\n".encode()
            client_socket.send(header_500)
            break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()

