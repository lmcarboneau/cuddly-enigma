#!/usr/bin/env python3
"""
Very simple HTTP server in python for requests
Usage::
	./theServer.py
"""

import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = ''
PORT_NUMBER = 80

class ThisHandler(BaseHTTPRequestHandler):
  def do_HEAD(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json; charset=utf-8')
    self.end_headers()

  def do_GET(self):
    paths = {
      '/status': {'status':200}
    }

    if self.path in paths:
      self.respond(paths[self.path])
    else:
      file_handler = open('index.html', 'rb')
      response_content = file_handler.read()
      file_handler.close()
      self.respond({'status':200, 'content':response_content})

  def do_PUT(self):
    content_length = int(self.headers['Content-length'])
    post_data = self.rfile.read(content_length)

    self.respond({'status':503, 'content': post_data})

  def handle_http(self, status_code, content = ''):
    self.send_response(status_code)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    content = '{}'.format(content)
    return bytes(content, 'UTF-8')

  def respond(self, opts):
    if 'content' in opts:
      response = self.handle_http(opts['status'], opts['content'])
    else:
      response = self.handle_http(opts['status'])
    self.wfile.write(response)

if __name__ == '__main__':
  server_class = HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), ThisHandler)
  print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))

