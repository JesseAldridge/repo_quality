import json, re

import requests

import config, l0_repo


def pull(url=None, count=20):
  if url is None:
    url = 'https://api.github.com/search/repositories?q=stars:>1&s=stars&order=desc'
  print 'requesting:', url
  resp = requests.get(url, auth=config.auth_)

  results_dict = json.loads(resp.content)
  for repo_dict in results_dict['items']:
    l0_repo.write_repo(repo_dict)

  print 'rate-limit remaining:', resp.headers['x-ratelimit-remaining']
  next_link = re.search('<(.+?)>', resp.headers['link']).group(1)
  if count > 0:
    count -= 1
    pull(next_link, count)

def parse():
  with open('most_starred.json') as f:
    json_str = f.read()
  most_starred = json.loads(json_str)
  print 'num:', len(most_starred['items'])

if __name__ == '__main__':
  pull()
