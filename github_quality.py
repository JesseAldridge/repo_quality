import json, os, re, getpass

import requests, arrow
from requests import auth

import secrets, config

if not os.path.exists(config.cache_dir_path):
  os.mkdir(config.cache_dir_path)

class g:
  mean_stars_per_issue = 10

def pull_most_starred():
  resp = requests.get(
    'https://api.github.com/search/repositories?q=stars:>1&s=stars&order=desc')

  print json.dumps(json.loads(resp.content), indent=2)

  print 'rate-limit remaining:', resp.headers['x-ratelimit-remaining']
  next_link = re.search('<(.+?)>', resp.headers['link']).group(1)
  print 'next_link:', next_link

def pull_all():
  use_auth = True
  auth_ = auth.HTTPBasicAuth('JesseAldridge', secrets.api_key) if use_auth else None
  repo_dicts = []
  min_score, max_score = None, None
  stars_per_issue_list = []
  for path in [
    # libs that have worked well
    'twbs/bootstrap', 'kennethreitz/requests', 'jasmine/jasmine', 'rails/rails',
    'angular/angular.js', 'tax/python-requests-aws', 'django/django', 'mitsuhiko/flask',
    'npm/npm', 'asweigart/pyperclip', 'JesseAldridge/github_quality', 'fabric/fabric',

    # python unit testing libs
    'nose-devs/nose', 'gabrielfalcao/lettuce', 'pytest-dev/pytest', 'nose-devs/nose2',
    'docopt/docopt', 'gabrielfalcao/sure', 'rlisagor/freshen', 'behave/behave',

    # libs I haven't tried much
    'Microsoft/TypeScript', 'meteor/meteor', 'facebook/react', 'angular/angular',
    'strongloop/express', 'dscape/nano', 'Level/levelup', 'felixge/node-mysql',
    'mongodb/node-mongodb-native', 'brianc/node-postgres', 'NodeRedis/node_redis',
    'mapbox/node-sqlite3', 'mafintosh/mongojs', 'tornadoweb/tornado', 'gevent/gevent',
    'percolatestudio/meteor-migrations', 'Polymer/polymer', 'Automattic/mongoose',
    'nodejs/node', 'sequelize/sequelize', 'Automattic/monk', 'balderdashy/waterline',
    'balderdashy/sails', 'playframework/playframework', 'pyinvoke/invoke',
    'msanders/snipmate.vim',

    # libs that have given me trouble
    'sindresorhus/atom-jshint', 'angular-ui-tree/angular-ui-tree',
    'boto/boto', 'rupa/z', 'lsegal/atom-runner'
    ]:
    repo_dict = pull_repo(path, auth=auth_)
    if min_score is None or repo_dict['score'] < min_score:
      min_score = repo_dict['score']
    if max_score is None or repo_dict['score'] > max_score:
      max_score = repo_dict['score']
    stars_per_issue_list.append(float(repo_dict['stargazers_count'] / repo_dict['issue_count']))
    if not repo_dict:
      print 'null repo:', path, repo_dict
    repo_dicts.append(repo_dict)
  g.mean_stars_per_issue = (
    sum(stars_per_issue_list) / float(len(stars_per_issue_list))
    if stars_per_issue_list else g.mean_stars_per_issue)

  json_out = json.dumps({'min_score': min_score, 'max_score': max_score}, indent=2)
  with open(os.path.join(config.cache_dir_path, 'min_max.json'), 'w') as f:
    f.write(json_out)

  for repo_dict in sorted(repo_dicts, key=lambda d: -d['score']):
    print '        path:', repo_dict['path']
    print '       stars:', repo_dict['stargazers_count']
    print '      issues:', repo_dict['open_issues_count']
    print '  has_issues:', repo_dict['has_issues']
    print '         age:', repo_dict['age']
    print 'stars/issues:', repo_dict['stargazers_count'] / (repo_dict['open_issues_count'] or 1)
    print '   stars/age:', repo_dict['stargazers_count'] / (repo_dict['age'].days or 1)
    print '       score:', repo_dict['score']
    print

  printed_suck_line = False
  for repo_dict in sorted(repo_dicts, key=lambda d: -d['score']):
    if repo_dict['score'] < 180 and not printed_suck_line:
      printed_suck_line = True
      print '-------  suck line -------'
    print repo_dict['path']
    print ' ', repo_dict['score']


hardcoded_issue_counts = {
  'django/django': 1209,
  # (node-mongodb's jira page only lists 14 issues; but you have to make an account to create an
  #  issue, so I'm assuming that if they used GitHub issues they would have 10x more.)
  'mongodb/node-mongodb-native': 140
}

def pull_repo(path, auth=None):
  if not re.match('[A-Za-z0-9_/-]+', path):
    return 'illegal char in path'
  if len(path) > 100:
    return 'path too long'
  cache_file_path = os.path.join(config.cache_dir_path, path.replace('/', '_') + '.txt')
  if not os.path.exists(cache_file_path):
    print 'pulling info:', cache_file_path
    resp = requests.get('https://api.github.com/repos/' + path, auth=auth)
    print 'xrate-limit-remaining:', resp.headers['x-ratelimit-remaining']
    if 'created_at' in resp.content:
      with open(cache_file_path, 'w') as f:
        f.write(json.dumps(json.loads(resp.content), indent=2))

  with open(cache_file_path) as f:
    repo_dict = json.loads(f.read())

  repo_dict['path'] = path
  repo_dict['age'] = arrow.now() - arrow.get(repo_dict['created_at'])
  repo_dict['score'] = (
    repo_dict['stargazers_count'] * .01 +
    repo_dict['stargazers_count'] / repo_dict['age'].days * 2)

  # (need to hardcode issue counts for projects which don't use github for issues)
  print 'mean_stars_per_issue:', g.mean_stars_per_issue
  if repo_dict['has_issues']:
    issue_count = repo_dict['open_issues_count']
  elif path in hardcoded_issue_counts:
    issue_count = hardcoded_issue_counts[path]
  else:
    issue_count = repo_dict['stargazers_count'] / g.mean_stars_per_issue
  repo_dict['issue_count'] = issue_count
  repo_dict['score'] += repo_dict['stargazers_count'] / (issue_count or 1) * 20
  return repo_dict

if __name__ == '__main__':
  pull_all()
