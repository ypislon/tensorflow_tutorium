from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import time
# import prototype as pt_img
from urllib.parse import urlparse, parse_qs
import cgi
import re

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = self.path
        if self.path == "/":
            self.path = "/index.html"

        try:
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True

            if sendReply == True:
                try:
                    ## 'rb' is used for encoding the file as a binary string
                    ## see: https://stackoverflow.com/questions/10971033/backporting-python-3-openencoding-utf-8-to-python-2
                    ## also: https://stackoverflow.com/questions/33054527/python-3-5-typeerror-a-bytes-like-object-is-required-not-str-when-writing-t
                    r = open(curdir + sep + self.path, 'rb')
                except OSError:
                    self.send_error(404, 'Error while reading file %s' % self.path)
                    return
                print(r)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(r.read())
                r.close()

            return
        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)

    def deal_post_data(self):
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        print(line.decode())
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        print("problem:")
        print(fn)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def parse_POST(self):
        postvars = {}
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            r, info = self.deal_post_data()
            print(info)
            # temp_postvars = cgi.parse_multipart(self.rfile, pdict)
            # print(temp_postvars)
            # for key, value in temp_postvars.items():
            #     newKey = key.decode('utf-8')
            #     newValue = value[0].decode('utf-8')
            #     postvars[newKey] = newValue
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            temp_postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            for key, value in temp_postvars.items():
                newKey = key.decode('utf-8')
                newValue = value[0].decode('utf-8')
                postvars[newKey] = newValue
        return postvars

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        postvars = self.parse_POST()
        print ('postvars:')
        print(postvars)
        # get posted data
        # post_data = self.rfile.read(content_length)
        # post_data = post_data.decode('utf-8')

        self.send_response(200)
        self.end_headers()
        return

    do_GET = do_GET
    do_POST = do_POST

def run():
    PORT = 44444
    print('Starting up server on port %s...' % PORT)
    server = HTTPServer(('localhost', PORT), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print (time.asctime(), "Server Stopped")

run()
