import time

import requests
from werkzeug import exceptions

class PullFailed(Exception):
  pass

class FailedSeveralTimes(Exception):
  pass

def hit_api(repo_path, auth, suffix=''):
  main_resp = requests.get('https://api.github.com/repos/{}{}'.format(repo_path, suffix), auth=auth)
  for _ in range(10):
    if main_resp.status_code == 200:
      print 'main xrate-limit-remaining:', main_resp.headers['x-ratelimit-remaining']
      return main_resp.content
    elif main_resp.status_code == 404:
      print 'repo not found: {}'.format(repo_path)
      raise exceptions.NotFound()
    elif main_resp.status_code == 403:
      reset_time = main_resp.headers['X-RateLimit-Reset']
      print 'rate limit exceeded, sleeping for 60 seconds, reset_time:', reset_time
      time.sleep(60)
    else:
      print 'pull failed:', main_resp.status_code
      print '  resp:', main_resp.content[:100]
      raise PullFailed()
  else:
    raise FailedSeveralTimes()

if __name__ == '__main__':
  print hit_api('hapijs/hapi', None)
