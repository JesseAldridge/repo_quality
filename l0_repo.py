import re, json, os, time

import requests

import config


class IllegalCharException(Exception):
  pass

class PathLengthException(Exception):
  pass

class BadRepoException(Exception):
  pass

def validate_path(path):
  if not re.match('[A-Za-z0-9_/-]+', path):
    raise IllegalCharException()
  if len(path) > 100:
    raise PathLengthException()

def write_repo(repo_dict):
  path = repo_dict['full_name']
  validate_path(path)
  cache_file_path = os.path.join(config.cache_dir_path, path.replace('/', '_')) + '.txt'
  if 'created_at' not in repo_dict:
    raise BadRepoException()
  with open(cache_file_path, 'w') as f:
    f.write(json.dumps(repo_dict, indent=2))
  return cache_file_path

if __name__ == '__main__':
  def test():
    resp = requests.get('https://api.github.com/repos/twbs/bootstrap')
    cache_file_path = write_repo(json.loads(resp.content))
    mod_time = os.path.getmtime(cache_file_path)
    assert time.time() - mod_time < 1, time.time() - mod_time
  test()
