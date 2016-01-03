import json, re

import requests

def pull():
  resp = requests.get(
    'https://api.github.com/search/repositories?q=stars:>1&s=stars&order=desc')

  results_dict = json.loads(resp.content)
  for repo_dict in results_dict.items
  print json.dumps(results_dict, indent=2)

  print 'rate-limit remaining:', resp.headers['x-ratelimit-remaining']
  next_link = re.search('<(.+?)>', resp.headers['link']).group(1)
  print 'next_link:', next_link

def parse():
  with open('most_starred.json') as f:
    json_str = f.read()
  most_starred = json.loads(json_str)
  print 'num:', len(most_starred['items'])

if __name__ == '__main__':
  parse()