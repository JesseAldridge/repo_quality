import json, os, re

import requests, arrow

def pull_most_starred():
  resp = requests.get(
    'https://api.github.com/search/repositories?q=stars:>1&s=stars&order=desc')

  print json.dumps(json.loads(resp.content), indent=2)

  print 'rate-limit remaining:', resp.headers['x-ratelimit-remaining']
  next_link = re.search('<(.+?)>', resp.headers['link']).group(1)
  print 'next_link:', next_link


if not os.path.exists('cache'):
  os.mkdir('cache')

repo_dicts = []
for path in [
  # libs that have worked well
  'twbs/bootstrap', 'kennethreitz/requests', 'jasmine/jasmine', 'rails/rails',
  'angular/angular.js', 'tax/python-requests-aws', 'django/django', 'mitsuhiko/flask',
  'npm/npm', 'asweigart/pyperclip',

  # libs I haven't tried
  'Microsoft/TypeScript', 'meteor/meteor', 'facebook/react', 'angular/angular',

  # libs that have given me trouble
  'sindresorhus/atom-jshint', 'angular-ui-tree/angular-ui-tree',
  'boto/boto', 'rupa/z', 'lsegal/atom-runner']:
  cache_path = os.path.join('cache', path.replace('/', '_') + '.txt')
  if not os.path.exists(cache_path):
    print 'pulling info:', cache_path
    resp = requests.get('https://api.github.com/repos/' + path)
    with open(cache_path, 'w') as f:
      f.write(json.dumps(json.loads(resp.content), indent=2))

  with open(cache_path) as f:
    repo_dict = json.loads(f.read())

  repo_dict['path'] = path
  repo_dict['age'] = arrow.now() - arrow.get(repo_dict['created_at'])
  repo_dict['score'] = (
    repo_dict['stargazers_count'] * .01 +
    repo_dict['stargazers_count'] / repo_dict['age'].days * 2)

  # (need to hardcode issue counts for projects which don't use github for issues)
  issue_count = (
    repo_dict['open_issues_count'] if repo_dict['has_issues'] else
    {'django/django':1209}[path])
  repo_dict['score'] += repo_dict['stargazers_count'] / issue_count * 20
  repo_dicts.append(repo_dict)

for repo_dict in sorted(repo_dicts, key=lambda d: -d['score']):
  print '        path:', repo_dict['path']
  print '       stars:', repo_dict['stargazers_count']
  print '      issues:', repo_dict['open_issues_count']
  print '  has_issues:', repo_dict['has_issues']
  print '         age:', repo_dict['age']
  print 'stars/issues:', repo_dict['stargazers_count'] / repo_dict['open_issues_count']
  print '   stars/age:', repo_dict['stargazers_count'] / repo_dict['age'].days
  print '       score:', repo_dict['score']
  print

printed_suck_line = False
for repo_dict in sorted(repo_dicts, key=lambda d: -d['score']):
  if repo_dict['score'] < 600 and not printed_suck_line:
    printed_suck_line = True
    print '-------  suck line -------'
  print repo_dict['path']
  print ' ', repo_dict['score']
