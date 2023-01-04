import os
import yaml
from yaml import Loader
from server.config import ServerConfig
import json

def print_responses(responses):
  print(json.dumps(responses, sort_keys=True, indent=4))

def read(path):
  if not os.path.exists(path):
    raise Exception("No such file: {}".format(path))

  with open(path) as f:
    data = yaml.load(f, Loader=Loader)
    endpoints = data['paths']
    responses = dict()
    requests = dict()
    print("Found: {} endpoints.".format(len(endpoints)))
    
    for idx, endpoint in enumerate(endpoints):
      verbs = [str(verb) for verb in data['paths'][endpoint].keys()]
      responses[str(endpoint).strip()] = dict()
      requests[str(endpoint).strip()] = dict()

      # Iterate over allowed verbs
      for verb in verbs:
        for stat in data['paths'][endpoint][verb]:
          responses[str(endpoint).strip()][verb] = data['paths'][endpoint][verb]['responses']
          if 'requestBody' in  data['paths'][endpoint][verb].keys():
            requests[str(endpoint).strip()][verb] = data['paths'][endpoint][verb]['requestBody']
          else:
            requests[str(endpoint).strip()][verb] = dict()

      print("* {} - {} \n\t Allowed methods: {}".format(idx, endpoint, verbs))

    # print_responses(responses)
  return responses, requests
    
