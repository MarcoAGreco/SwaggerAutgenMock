import sys
from swagger.reader import read
from server.mock import start_server

def main():
  print("\n --- Swagger - Automock ---")
  
  if(len(sys.argv )!= 2):
    help()
    exit(-1)
  filename = sys.argv[1]

  print("Reading swagger: {}".format(filename))
  mocked_responses, requests = read(filename)
  start_server(mocked_responses, requests)


def help():
  print("Type: gen_mock.py <SWAGGER_FILE>.yaml")

if __name__ == "__main__":
  main()
