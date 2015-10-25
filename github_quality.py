import json, os

import requests, arrow

if not os.path.exists('cache'):
  os.mkdir('cache')

repo_dicts = []
for path in [
  'twbs/bootstrap', 'kennethreitz/requests', 'jasmine/jasmine', 'rails/rails',
  'meteor/meteor', 'facebook/react', 'angular/angular.js', 'angular/angular',
  'tax/python-requests-aws',

  'sindresorhus/atom-jshint', 'npm/npm', 'angular-ui-tree/angular-ui-tree', 'boto/boto',
  'karma-runner/karma', 'rupa/z', 'lsegal/atom-runner']:
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
    repo_dict['stargazers_count'] / repo_dict['open_issues_count'] * 20 +
    repo_dict['stargazers_count'] / repo_dict['age'].days * 2)
  repo_dicts.append(repo_dict)

for repo_dict in sorted(repo_dicts, key=lambda d: -d['score']):
  print '       path:', repo_dict['path']
  print '      stars:', repo_dict['stargazers_count']
  print '     issues:', repo_dict['open_issues_count']
  print '        age:', repo_dict['age']
  print 'star/issues:', repo_dict['stargazers_count'] / repo_dict['open_issues_count']
  print '   star/age:', repo_dict['stargazers_count'] / repo_dict['age'].days
  print '      score:', repo_dict['score']
  print

printed_suck_line = False
for repo_dict in sorted(repo_dicts, key=lambda d: -d['score']):
  if repo_dict['score'] < 600 and not printed_suck_line:
    printed_suck_line = True
    print '-------  suck line -------'
  print repo_dict['path']
  print ' ', repo_dict['score']
