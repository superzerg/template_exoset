from os.path import isdir
from os import listdir
import requests
from sys import argv

def get_directory_to_compile(repository, pull_request_number, access_token):
  
  token = 'token '+ access_token
  url = 'https://api.github.com/repos/' + repository + '/pulls/'+ str(pull_request_number) + '/files'
  x = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json', 'authorization': token})
  filename_list = [jsondict['filename'] for jsondict in x.json()]
  directory_list = set()
  rerun_all = False
  for filename in filename_list:
    temp_filename = filename.split('/')[0]
    if temp_filename.startswith('.'):
      continue
    if isdir(temp_filename):
      if temp_filename == 'cartouche':
        rerun_all = True
        break
      else:
        directory_list.add(temp_filename)   
    else:
      rerun_all = True
      break
  if rerun_all:
    valid_dirs = [f for f in listdir('.') if isdir(f) and f != 'cartouche' and not f.startswith('.')]
    return valid_dirs
  else:
    return directory_list
           
      
if __name__ == '__main__':
  repository = argv[1]
  pr = argv[2]
  token = argv[3]
  directory_list = get_directory_to_compile(repository, pr, token)
  print('<ul>'+ ' '.join(['<li>' + d + '<\li>' for d in directory_list]) + '</ul>')
  
