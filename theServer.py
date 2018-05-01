#!/usr/bin/env python3
"""
Very simple HTTP server in python for requests
Usage::
	./theServer.py
"""

import time
import os
import fnmatch
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
      '/status': {'status':200}, 
      '/images': {'status':200}
    }

    if self.path == '/images':
      imagefiles = []
      for filename in os.listdir(os.getcwd()):
        if fnmatch.fnmatch(filename, '*.jpg'):
          imagefiles.append('<a href="uas-at-fgcu.com/' + filename + '"></a><br>')
      if not imagefiles:
        imagestr = 'No images found'
      else:
        imagestr = ''.join(imagefiles)
      self.respond({'status':200, 'content': '!DOCTYPE html>   <html lang="en">    <title>UAS at FGCU </title>    <meta name="viewport" content="width=device-width, initial-scale=1">    <link rel="stylesheet" href="https://unpkg.com/tachyons/css/tachyons.min.css">    <body>     <header class="bg-black-90 fixed w-100 ph3 pv3 pv4-ns ph4-m ph5-l">      <nav class="f6 fw6 ttu tracked">       <a class="link dim white dib mr3" href="http://arduino.fgcu.edu/" title="Home">Arduino at FGCU Home</a>      </nav>     </header>      <section class="flex-ns vh-100 items-center">        '
		      + imagestr + '<a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib black" href="uas-at-fgcu.com/images">           View Images         </a>        </div>      </section>     <footer class="pv4 ph3 ph5-m ph6-l mid-gray">      <small class="f6 db tc">Ã‚Â© 2018 <b class="ttu">Software Engineering at Florida Gulf Coast University</b>., All Rights Reserved</small>     </footer>    </body>  </html>    '})
    if self.path in paths:
      self.respond(paths[self.path])
    elif self.path.endswith(".jpg"):
      f = open(self.path, 'rb')
      self.send_header('Content-type', 'image/png')
      self.end_headers()
      self.wfile.write(f.read())
      f.close()
    else:
      file_handler = open('index.html', 'rb')
      response_content = file_handler.read()
      file_handler.close()
      response_content = "".join(map(chr,response_content)).replace('\n', ' ').replace('\r', ' ').replace('b\'','')
      
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

