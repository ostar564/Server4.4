# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os
import codecs
from urllib.parse import unquote
from PIL import Image
# constants
IP = '127.0.0.1'
PORT = 8080
SOCKET_TIMEOUT = 20
REDIRECTION_DICTIONARY = {'index1.html': 'index.html'}
CONTENT_TYPE = {"html": "text/html; charset=utf-8",
                "txt": "text/html; charset=utf-8",
                "jpg": "image/jpeg",
                "png": "image/jpeg",
                "js": "text/javascript; charset=UTF-8",
                "css": "text/css",
                "ico": "image/x-icon",
                "gif": "image/gif"}


def handle_client_request(resource, client_socket, client_request):
    """ Check the required resource, generate proper HTTP response and send to client"""
    project_name = "C:\\Users\\User\\Documents\\עומר סייבר\\סייבר"
    filename = project_name
    split_recourse = resource.split("\\")
    for part in split_recourse[1:]:
        filename += '\\' + part
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
        header_302 = "HTTP/1.1 302\r\n" + "Location:" + filename[
                                                        len(filename): len(filename) - filename[::-1].index("\\")] + \
                     REDIRECTION_DICTIONARY[name] + "\r\n\r\n"
        header_302 = header_302.encode('UTF-8')
        client_socket.send(header_302)
    elif split_recourse[-1].startswith("calculate-next"):
        num_split = split_recourse[-1].split('=')
        num = int(num_split[-1])
        num += 1
        data2 = str(num)
        http_header_calcn = "HTTP/1.1 200\r\n"
        http_header_calcn += f"Content-Length:{len(data2)}\r\n"
        http_header_calcn += "Content-Type: text/plain\r\n"
        http_header_calcn += "\r\n"
        http_response = http_header_calcn.encode('UTF-8')
        http_response += data2.encode('UTF-8')
        client_socket.send(http_response)
    elif split_recourse[-1].startswith("calculate-area"):
        num_split = split_recourse[-1].split('&')
        num_split2 = num_split[1].split('=')
        w = int(num_split2[1])
        num_split3 = num_split[0].split('=')
        h = int(num_split3[1])
        dataReturn = str(h * w / 2)
        http_header_calcA = "HTTP/1.1 200\r\n"
        http_header_calcA += f"Content-Length:{len(dataReturn)}\r\n"
        http_header_calcA += "Content-Type: text/plain\r\n"
        http_header_calcA += "\r\n"
        http_response = http_header_calcA.encode('UTF-8')
        http_response += dataReturn.encode('UTF-8')
        client_socket.send(http_response)
    elif split_recourse[-1].startswith("image?image-name"):
        name_for_file = name.split("=")[1]
        path = ""
        for part in split_recourse[1:]:
            if not part.startswith('image?image-name'):
                path += '\\' + part
        final_path = project_name + "\\htttp_server_omer_jonathan_ofek\\webroot" + "\\uploads\\" + name_for_file
        print("final path", final_path)
        if os.path.isfile(final_path):
            print("yes")
            data = get_file_data(final_path)
            http_header = "HTTP/1.1 200\r\n"
            http_header += f"Content-Length: {(os.path.getsize(final_path))}\r\n"
            http_header += f"Content-Type: {content_type(final_path)}\r\n"
            http_header += "\r\n"
            http_response = http_header.encode('UTF-8')
            if isinstance(data, bytes):
                http_response += data
            else:
                http_response += data.encode('UTF-8')
            client_socket.send(http_response)
        else:
            header_404 = "HTTP/1.1 404 \r\n\r\n".encode()
            client_socket.send(header_404)
    elif name.startswith("upload?"):
        name_for_file = name.split("=")[1]
        path = ""
        for part in split_recourse[1:]:
            if not part.startswith('upload?'):
                path += '\\' + part
        print("client request", client_request)
        header = client_request.split('\r\n'.encode())
        content_length = 0
        for field in header:
            if field.startswith('Content-Length'.encode()):
                print(field)
                content_length = int(field.split(':'.encode())[1].strip())
        print(content_length)
        # with open(project_name + path + "\\uploads\\" + unquote(name_for_file), "wb") as file:
        #     length_datasend = 0
        #     data = client_socket.recv(content_length)
        #     length_datasend += len(data)
        #     print(length_datasend)
        #     file.write(data)
        #     file.close()
        im = Image.open(project_name + path + "\\uploads\\" + unquote(name_for_file), "wb")
        data = client_socket.recv(content_length)
        im.write(data)
        im.close()
        http_header_post = "HTTP/1.1 200\r\n\r\n"
        client_socket.send(http_header_post.encode())
    else:
        header_404 = "HTTP/1.1 404 \r\n\r\n".encode()
        client_socket.send(header_404)


def get_file_data(filename):
    """
    :param filename:
    :return: Gets file path and returns it's content
    """
    file = codecs.open(filename, "rb")
    str1 = file.read()
    file.close()
    return str1


def content_type(filename):
    """
    :param filename:
    :return: type of file
    """
    name = filename[len(filename) - filename[::-1].index("."):len(filename)]
    return CONTENT_TYPE[name]


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    print(request)
    split_request = request.split("\r\n".encode())[0].split(" ".encode())
    for i in range(len(split_request)):
        split_request[i] = split_request[i].decode()
    post_encoded = ""
    if (split_request[0] == 'GET' or split_request[0] == 'POST') and split_request[2].startswith('HTTP/1.1') and len(
            split_request) >= 3:
        request_url = split_request[1].replace("/", "\\")
        x = (True, request_url)
        return x
    y = (False, None)
    return y


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    # TO DO: insert code that receives client request
    # get client request
    client_request = client_socket.recv(1024)
    valid_http, resource = validate_http_request(client_request)
    if valid_http:
        print('Got a valid HTTP request')
        handle_client_request(resource, client_socket, client_request)
    else:
        print('Error: Not a valid HTTP request')
        header_500 = "HTTP/1.1 500 \r\n\r\n".encode()
        client_socket.send(header_500)
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
