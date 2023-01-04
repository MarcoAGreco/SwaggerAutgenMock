from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from jsf import JSF
import jsonschema
from jsonschema import validate

HOSTNAME = "localhost"
MOCK_CASE_HEADER = 'X-Mock-Case'
serverConf = {}
reqs = {}

def validate_req(schema, req):
  validate(instance=req, schema=schema)

    
def handler(req_handler, method='get'):
  endpoint = str(req_handler.path)
  case = 0

  if endpoint in serverConf.keys():
    if method in serverConf[endpoint].keys():

      # Check if case switch value is present
      if MOCK_CASE_HEADER in req_handler.headers:
        case = int(req_handler.headers[MOCK_CASE_HEADER])
        if case >= len(serverConf[endpoint][method]):
          case = 0
      
      status = list(serverConf[endpoint][method].keys())[case]

      if method == 'post' or method == 'put' or method == 'patch':
        try:
          schemaReq = reqs[endpoint][method]['content']['application/json']['schema']
          if schemaReq:
            content_len = int(req_handler.headers.get('Content-Length'))
            body_req = json.loads(req_handler.rfile.read(content_len).decode("utf-8"))
            validate_req(schemaReq, body_req)

        except (json.decoder.JSONDecodeError, jsonschema.exceptions.ValidationError):
          req_handler.send_response(400)
          req_handler.send_header("Content-type", "text/html")
          req_handler.end_headers()
          req_handler.wfile.write(bytes("<html><head><title>Error 400 - BAD REQUEST</title></head>", "utf-8"))
          req_handler.wfile.write(bytes("<body></body></html>", "utf-8"))
          return

      req_handler.send_response(int(status))
      req_handler.send_header("Content-type", "application/json")
      req_handler.end_headers()
      
      # Generate fake data from schema
      schema = serverConf[endpoint][method][status]['content']['application/json']['schema']
      fake_data_gen  = JSF(schema)

      req_handler.wfile.write(bytes(json.dumps(fake_data_gen.generate()), "utf-8"))
    
    else:
      req_handler.send_response(405)
      req_handler.send_header("Content-type", "text/html")
      req_handler.end_headers()
      req_handler.wfile.write(bytes("<html><head><title>Error 405 - METHOD NOT ALLOWED</title></head>", "utf-8"))
      req_handler.wfile.write(bytes("<body></body></html>", "utf-8"))
  else:
    req_handler.send_response(404)
    req_handler.send_header("Content-type", "text/html")
    req_handler.end_headers()
    req_handler.wfile.write(bytes("<html><head><title>Error 404 - NOT FOUND</title></head>", "utf-8"))
    req_handler.wfile.write(bytes("<body></body></html>", "utf-8"))

class MockServer(BaseHTTPRequestHandler):
  def do_GET(self):
    handler(self, 'get')
        
  def do_POST(self):
    handler(self, 'post')

  def do_DELETE(self):
    handler(self, 'delete')

  def do_PUT(self):
    handler(self, 'put')

  def do_PATCH(self):
    handler(self, 'patch')

def start_server(responses, requests, port=8080):
    global serverConf
    global reqs
    reqs = requests
    serverConf = responses
    webServer = HTTPServer((HOSTNAME, port), MockServer)
    print("Server started http://%s:%s" % (HOSTNAME, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
