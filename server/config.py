class ServerConfig:
  """Server config data"""

  def __init__(self, endpoints, responses):
    self.endpoints = endpoints
    self.responses = responses

class Response:
  """Server mocked response"""

  def __init__(self, status, body):
    self.status = status
    self.body = body