import json, os, re, getpass

import requests, arrow
from requests import auth

cache_dir_path = os.path.expanduser('~/.github_quality')
if not os.path.exists(cache_dir_path):
  os.mkdir(cache_dir_path)

def pull_most_starred():
  resp = requests.get(
    'https://api.github.com/search/repositories?q=stars:>1&s=stars&order=desc')

  print json.dumps(json.loads(resp.content), indent=2)

  print 'rate-limit remaining:', resp.headers['x-ratelimit-remaining']
  next_link = re.search('<(.+?)>', resp.headers['link']).group(1)
  print 'next_link:', next_link

def pull_all():
  use_auth = False
  auth_ = auth.HTTPBasicAuth('JesseAldridge', getpass.getpass()) if use_auth else None
  repo_dicts = []
  for path in [
    # libs that have worked well
    # 'twbs/bootstrap', 'kennethreitz/requests', 'jasmine/jasmine', 'rails/rails',
    # 'angular/angular.js', 'tax/python-requests-aws', 'django/django', 'mitsuhiko/flask',
    # 'npm/npm', 'asweigart/pyperclip', 'JesseAldridge/github_quality', 'fabric/fabric',

    # python unit testing libs
    'nose-devs/nose', 'gabrielfalcao/lettuce', 'pytest-dev/pytest', 'nose-devs/nose2',
    'docopt/docopt', 'gabrielfalcao/sure', 'rlisagor/freshen',

    # libs I haven't tried much
    # 'Microsoft/TypeScript', 'meteor/meteor', 'facebook/react', 'angular/angular',
    # 'strongloop/express', 'dscape/nano', 'Level/levelup', 'felixge/node-mysql',
    # 'mongodb/node-mongodb-native', 'brianc/node-postgres', 'NodeRedis/node_redis',
    # 'mapbox/node-sqlite3', 'mafintosh/mongojs', 'tornadoweb/tornado', 'gevent/gevent',
    # 'percolatestudio/meteor-migrations', 'Polymer/polymer', 'Automattic/mongoose',
    # 'nodejs/node', 'sequelize/sequelize', 'Automattic/monk', 'balderdashy/waterline',
    # 'balderdashy/sails', 'playframework/playframework', 'pyinvoke/invoke',

    # libs that have given me trouble
    # 'sindresorhus/atom-jshint', 'angular-ui-tree/angular-ui-tree',
    # 'boto/boto', 'rupa/z', 'lsegal/atom-runner'
    ]:
    repo_dict = pull_repo(path, auth=auth_)
    if not repo_dict:
      print 'null repo:', path, repo_dict
    repo_dicts.append(repo_dict)

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


def pull_repo(path, auth=None):
  if not re.match('[A-Za-z0-9_\-]+', path):
    return 'illegal char in path'
  if len(path) > 100:
    return 'path too long'
  cache_file_path = os.path.join(cache_dir_path, path.replace('/', '_') + '.txt')
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
  issue_count = (
    repo_dict['open_issues_count'] if repo_dict['has_issues'] else
    {'django/django':1209,
    # (node-mongodb's jira page only lists 14 issues; but you have to make an account to create an
    #  issue, so I'm assuming that if they used GitHub issues they would have 10x more.)
    'mongodb/node-mongodb-native':140}[path])
  repo_dict['score'] += repo_dict['stargazers_count'] / (issue_count or 1) * 20
  return repo_dict

if __name__ == '__main__':
  pull_all()
