#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Abram Hindle, Alex Mak, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def prepare_request(self, url):
        # Goal: prepare the http request to be sent later by setting up the url, hostname, port, path
        
        # Setup url:
        # Just incase: add "http://" if it is not in the beginning of the url
        if 'http://' != url[0:7]:
            url="http://"+url 

        # get the url's info(hostname, port, path) using urlluib.urlparse(), learned from the source below
        
        # Source Title: urllib.parse — Parse URLs into components
        # Source Type: Website
        # Source author: Python Software Foundation Authors
        # Source License: Python Software Foundation License Version 2
        # Latest date contributed: February 9th, 2023
        # URL: https://docs.python.org/3/library/urllib.parse.html   

        hostname=urllib.parse.urlparse(url).hostname
        port=urllib.parse.urlparse(url).port

        # Incase if port doesn't exist, default it with 80
        # if port is None: // one or another below
        if not port: 
            port=80
            
        path=urllib.parse.urlparse(url).path

        # Incase if empty path/ path not exist, default it just with the slash
        if not path:
            path='/'
        
        # connect the server with the proper hostname and port number
        self.connect(hostname, port)
   
        # Return the info obtained
        return hostname, port, path

    def get_data(self):
        # Get the data first
        data=self.recvall(self.socket)
        # learned from lab to always close the socket right after reading data
        self.close()

        # Get code, body, header from get getter functions
        code=self.get_code(data)
        header=self.get_headers(data)
        body=self.get_body(data)

        # Print the response in the format of header + line + body
        response_output=header+body
        print(response_output)

        return code, header, body

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        # Goal: return the code in integer format

        # Find the all the 3-digit number using re.findall() method, return the first one found, learned from the source below
        
        # Source Title: Python Regex: re.search() VS re.findall()
        # Source Type: Website
        # Source author: Nikhil Aggarwal
        # Source License: CC BY-SA 
        # Latest date contributed: January 11th, 2022
        # URL: https://www.geeksforgeeks.org/python-regex-re-search-vs-re-findall/
        return int(re.findall(r'\d+\d+\d', data)[0])

    # Todo: Done
    def get_headers(self,data):
        # Goal: return the header in string format

        # Split the data into 2 by using 2 lines, splited data will be in 2 parts(0: header, 1: body)
        parts=data.split("\r\n\r\n")
        # Return the header part
        return parts[0]

    # Todo: Done
    def get_body(self, data):
        # Goal: return the body in string format

        # like get_header, just return the other part
        parts=data.split("\r\n\r\n")
        # Return the body part
        return parts[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    # To do a GET, you need to get a request and send it first, then recv to get its data (include code, header, and body)
    # Then print the HTTP response 
    def GET(self, url, args=None):
        
        # Learned to do accept: */* to allow different mimetye server wants to return from the source below:
        
        # Source Title: What does 'Accept: */*' mean under Client section of Request Headers?
        # Source Type: Website (StackOverflow)
        # Source author and editor: MildlySerious (URL: https://stackoverflow.com/users/1728398/mildlyserious), Zze (URL: https://stackoverflow.com/users/3509591/zze)
        # Source License: CC BY-SA 4.0
        # Latest date contributed: August 11th, 2011
        # Resource URI: https://stackoverflow.com/questions/14772634/what-does-accept-mean-under-client-section-of-request-headers

        # 1. prepare the request by getting the hostname, port and path within the prepare_request() function
        hostname, port, path=self.prepare_request(url)

        # 2. Build the POST request in string and send it
        send=f'GET {path} HTTP/1.1\r\nHost: {hostname}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\nConnection: close\r\n\r\n'
        self.sendall(send)

        # 3. Get the code, header and body and print the response itself within the get_data function()
        code, header, body=self.get_data()

        # 4. Return the HTTP response
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # For a POST request: 
        # 1. prepare the request by getting the hostname, port and path within the prepare_request() function
        hostname, port, path=self.prepare_request(url)

        # ONLY FOR POST
        # 1a. check encoded_param and bytes length 
        
        # Use urllib.prase.urlencode() to find the encoded parameters, then use that to find its length to determine its byte length (needed for POST request)
        # I have learned to use the urllib.prase.urlencode() from the source below
        
        # Source Title: urllib.parse — Parse URLs into components
        # Source Type: Website
        # Source author: Python Software Foundation Authors
        # Source License: Python Software Foundation License Version 2
        # Latest date contributed: February 9th, 2023
        # URL: https://docs.python.org/3/library/urllib.parse.html   

        # If args exist, query it with args to get the encoded_param, else it will be an empty string
        if args:
            encoded_params=urllib.parse.urlencode(args)
        else:
            encoded_params=""
        
        # Bytes length= length of param
        bytes_len=len(encoded_params)

        # 2. Build the POST request in string and send it
        send=f'POST {path} HTTP/1.1\r\nHost: {hostname}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {bytes_len}\r\n\r\n{encoded_params}'
        self.sendall(send)
        
        # 3. Get the code, header and body and print the response itself within the get_data function()
        code, header, body=self.get_data()

        # 4. Return the HTTP response
        return HTTPResponse(code, body)

    # Main method to decide whether do POST or GET
    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
