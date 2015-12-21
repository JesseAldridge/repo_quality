import json, re

import requests

# resp = requests.get('https://api.github.com/repositories')

resp = requests.get(
  'https://api.github.com/search/repositories?q=stars:>1&s=stars&order=desc')

print json.dumps(json.loads(resp.content), indent=2)

print 'rate-limit remaining:', resp.headers['x-ratelimit-remaining']
next_link = re.search('<(.+?)>', resp.headers['link']).group(1)
print 'next_link:', next_link
