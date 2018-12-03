import json

import _0_hit_api

# resp = _0_hit_api.hit_api('hapijs/hapi', None, '/issues')
# resp = _0_hit_api.hit_api('hapijs/hapi', None)
# resp = _0_hit_api.hit_api('go-martini/martini', None, '/commits')

# print resp

commits = json.loads(_0_hit_api.hit_api('hapijs/hapi', None, '/commits'))
primary_author = None
if commits:
  author_to_count = {}
  for i, commit in enumerate(commits):
    if not commit['author']:
      continue
    author = commit['author']['login']
    author_to_count.setdefault(author, 0)
    author_to_count[author] += 1
  primary_author = max(author_to_count.items(), key=lambda t: t[1])[0]
print 'primary_author:', primary_author
