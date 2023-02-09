#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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
        # 1. setup url:

        # add "http://" if http is not in url
        if 'http' not in url:
            url="http://"+url

        # get the url's info(hostname, port, path) using url.parse, learned from the link below
        # https://docs.python.org/3/library/urllib.parse.html
        # print("test start")
        # print(urllib.parse.urlparse(url))
        # print("test end")

        hostname=urllib.parse.urlparse(url).hostname
        # print(hostname)
        port=urllib.parse.urlparse(url).port
        # print(port)
        # print(type(port))
        path=urllib.parse.urlparse(url).path
        # print(path)

        # if empty path, default it just with the slash
        if not path:
            path='/'
        
        # If port doesn't exist, default it with 80
        # if port is None: // one or another below
        if not port: 
            port=80

        # connect the server with the proper hostname and port number
        self.connect(hostname, port)

        return hostname, port, path

    def get_data(self):
        # get the data first
        data=self.recvall(self.socket)
        # learned from lab to always close right after reading data
        self.close()

        # 3. get code, body, header and return the http response
        # 3a. Code
        code=self.get_code(data)
        # 3b. Header Part
        header=self.get_headers(data)
        # 3c. body
        body=self.get_body(data)

        # print the response in the format of header + line + body
        response_output=header+body

        # print("output starts")
        print(response_output)
        # print("output ends")

        return code, header, body

        # # 4. return the response
        # return HTTPResponse(code, body)

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    # Get request: code, header, body

    # Todo: Done
    def get_code(self, data):
        # Goal: return the code in integer format

        # Find the first 3-digit number using re.findall() method
        # https://www.guru99.com/python-regular-expressions-complete-tutorial.html
        return int(re.findall(r'\d+\d+\d', data)[0])
        # return None

    # Todo: Done
    def get_headers(self,data):
        # Goal: return the header in string format

        # Split the data with 2 lines, splited data will be in 2 parts(0: header, 1: body)
        parts=data.split("\r\n\r\n")
        # Return the header part
        return parts[0]

        # old
        """
        header=""
        lines=data.split('\r\n')
        # Find the index until that blank line that seperate the header and body
        header_end=lines.index("")
        for i in range(0, header_end):
            header+=(lines[i]+"\r\n")
        """
        # Pure test
        # print("test a")
        # for i in range(len(exp)):
        #     print(i)
        #     print(exp[i])
        #     print(type(exp[i]))
        # # print(lines[0])
        # print("test b")

        # return header
        # return None

    # Todo
    def get_body(self, data):
        # Goal: return the body in string format

        # Split the data with 2 lines, splited data will be in 2 parts(0: header, 1: body)
        parts=data.split("\r\n\r\n")
        # Return the body part
        return parts[1]

        # Old: 
        """
        body=""
        # Split the lines in a list
        lines=data.split('\r\n')
        # Find the index until that blank line that seperate the header and body
        body_start=lines.index("")
        for i in range(body_start, len(lines)):
            body+=(lines[i]+"\r\n")
        """
        # return body
        # return None
    
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
        # code = 500
        # body = ""
        # print("hihi")

        # https://www.guru99.com/difference-get-post-http.html 
        # https://stackoverflow.com/questions/14772634/what-does-accept-mean-under-client-section-of-request-headers


        hostname, port, path=self.prepare_request(url)

        # send the request
        send=f'GET {path} HTTP/1.1\r\nHost: {hostname}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\nConnection: close\r\n\r\n'
        self.sendall(send)


        # 2. try to get data itself
        # data=self.recvall(self.socket)
        # self.close()

        code, header, body=self.get_data()

        """
        # 3. get code, body, header and return the http response
        # 3a. Code
        code=self.get_code(data)

        # 3b. Header Part
        header=self.get_headers(data)

        # 3c. body
        body=self.get_body(data)
        """

        # 4. return the response
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # code = 500
        # body = ""

        hostname, port, path=self.prepare_request(url)

        # 1a. check arg and bytes length (only for POST reqeust)
        # print("test")
        # print(urllib.parse.urlencode(args))

        # use urllib.prase.urlencode to find the arguments, use that find its length to determine its byte length
        if args!=None:
            encoded_args=urllib.parse.urlencode(args)
            bytes_len=len(encoded_args)
        else:
            encoded_args=args
            bytes_len=0

        print("args start")
        print(encoded_args)
        print("args end")


        # https://stackoverflow.com/questions/14772634/what-does-accept-mean-under-client-section-of-request-headers
        send=f'POST {path} HTTP/1.1\r\nHost: {hostname}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {bytes_len}\r\n\r\n{encoded_args}'
        self.sendall(send)
        
        code, header, body=self.get_data()

        """
        # 2. try to get data itself
        data=self.recvall(self.socket)
        self.close()

        # 3. get code, body, header and return the http response
        # 3a. Code
        code=self.get_code(data)

        # 3b. Header Part
        header=self.get_headers(data)

        # 3c. body
        body=self.get_body(data)

        print(header)
        print(body)
        """

        # 4. return the response
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
