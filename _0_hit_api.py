import time
from datetime import datetime

import requests
from werkzeug import exceptions

class PullFailed(Exception):
  pass

class FailedSeveralTimes(Exception):
  pass

def log(*a):
  print '{} {}'.format(datetime.now().isoformat(), ' '.join([str(a) for a in a]))

def hit_api(repo_path, auth, suffix='', priority_request=False):
  main_resp = requests.get('https://api.github.com/repos/{}{}'.format(repo_path, suffix), auth=auth)
  for _ in range(10):
    if main_resp.status_code == 403:
      reset_time = main_resp.headers['X-RateLimit-Reset']
      log('rate limit exceeded, sleeping for 120 seconds, reset_time:', reset_time)
      time.sleep(120)
    if main_resp.status_code == 200:
      if int(main_resp.headers['x-ratelimit-remaining']) < 1000 and not priority_request:
        reset_time = main_resp.headers['X-RateLimit-Reset']
        log('rate limit running out, sleeping for 60 seconds, reset_time:', reset_time)
        time.sleep(60)
      log('main xrate-limit-remaining:', main_resp.headers['x-ratelimit-remaining'])
      return main_resp.content
    elif main_resp.status_code == 404:
      log('repo not found: {}'.format(repo_path))
      raise exceptions.NotFound()
    else:
      log('pull failed:', main_resp.status_code)
      log('  resp:', main_resp.content[:100])
      raise PullFailed()
  else:
    raise FailedSeveralTimes()

if __name__ == '__main__':
  print hit_api('hapijs/hapi', None)
