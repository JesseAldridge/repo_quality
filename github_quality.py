import json, os, re, getpass, glob, time

import requests, arrow

from stuff import secrets
import config, l0_repo, soft_train

if not os.path.exists(config.cache_dir_path):
  os.mkdir(config.cache_dir_path)

class g:
  search_reset_time = None

def pull_paths(paths):
  mean_stars_per_issue = l0_repo.get_mean_stars_per_issue()
  repo_dicts = []
  min_score, max_score = None, None
  stars_per_issue_list = []
  for path in paths:
    try:
      repo_dict = pull_repo(path, mean_stars_per_issue, auth=config.auth_)
      if min_score is None or repo_dict['score'] < min_score:
        min_score = repo_dict['score']
      if max_score is None or repo_dict['score'] > max_score:
        max_score = repo_dict['score']
      stars_per_issue = (
        float(repo_dict['stargazers_count'] / repo_dict['issue_count'])
        if repo_dict['issue_count'] != 0 else repo_dict['stargazers_count'])
      stars_per_issue_list.append(stars_per_issue)
      if not repo_dict:
        print 'null repo:', path, repo_dict
      repo_dicts.append(repo_dict)
    except Exception as e:
      print 'error reading:', path
      print 'exception:', e
      continue

  mean_stars_per_issue = (
    sum(stars_per_issue_list) / float(len(stars_per_issue_list))
    if stars_per_issue_list else config.default_stars_per_issue)
  requests.patch(
    'https://repo-quality.firebaseio.com/.json?auth=' + secrets.firebase_token,
    data=json.dumps({
      'mean_stars_per_issue': mean_stars_per_issue,
      'min_score': min_score, 'max_score': max_score
    }))

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


class SearchAPI:
  def __init__(self):
    self.rate_limit, self.reset_time = None, None

  def can_use(self):
    return self.rate_limit is None or self.rate_limit > 0 or time.time() > self.reset_time

search_api = SearchAPI()
def pull_repo(repo_path, mean_stars_per_issue, auth=None):
  l0_repo.validate_path(repo_path)
  cache_file_path = os.path.join(config.cache_dir_path, repo_path.replace('/', '_') + '.txt')
  if not os.path.exists(cache_file_path):
    print 'pulling info:', cache_file_path
    main_resp = requests.get('https://api.github.com/repos/' + repo_path, auth=auth)
    if main_resp.status_code == 200:
      print 'main xrate-limit-remaining:', main_resp.headers['x-ratelimit-remaining']
      l0_repo.write_repo(main_resp.content, repo_path)

  with open(cache_file_path) as f:
    repo_dict = json.loads(f.read())

  if not 'closed_issues' in repo_dict and search_api.can_use():
    closed_resp = requests.get(
      'https://api.github.com/search/issues?q=repo:{}+is:issue+is:closed'.format(
        repo_path), auth=auth)
    search_api.rate_limit = int(closed_resp.headers['x-ratelimit-remaining'])
    search_api.reset_time = int(closed_resp.headers['x-ratelimit-reset'])
    print 'closed xrate-limit-remaining:', search_api.rate_limit
    if closed_resp.status_code == 200:
      repo_dict['closed_issues'] = json.loads(closed_resp.content)['total_count']
      l0_repo.write_repo(repo_dict)

  repo_dict['path'] = repo_path
  repo_dict['age'] = arrow.now() - arrow.get(repo_dict['created_at'])

  l0_repo.rate_repo(repo_dict, mean_stars_per_issue)
  return repo_dict

if __name__ == '__main__':
  paths = []
  for cache_file_path in glob.glob(os.path.join(config.cache_dir_path, '*.txt')):
    with open(cache_file_path) as f:
      repo_dict = json.loads(f.read())
    paths.append(repo_dict['full_name'])
  software_paths, _ = soft_train.classify(paths)
  pull_paths(software_paths)


  # pull_paths([
  #   # libs that have worked well
  #   'twbs/bootstrap', 'kennethreitz/requests', 'jasmine/jasmine', 'rails/rails',
  #   'angular/angular.js', 'tax/python-requests-aws', 'django/django', 'mitsuhiko/flask',
  #   'npm/npm', 'asweigart/pyperclip', 'JesseAldridge/github_quality', 'fabric/fabric',

  #   # python unit testing libs
  #   'nose-devs/nose', 'gabrielfalcao/lettuce', 'pytest-dev/pytest', 'nose-devs/nose2',
  #   'docopt/docopt', 'gabrielfalcao/sure', 'rlisagor/freshen', 'behave/behave',

  #   # libs I haven't tried much
  #   'Microsoft/TypeScript', 'meteor/meteor', 'facebook/react', 'angular/angular',
  #   'strongloop/express', 'dscape/nano', 'Level/levelup', 'felixge/node-mysql',
  #   'mongodb/node-mongodb-native', 'brianc/node-postgres', 'NodeRedis/node_redis',
  #   'mapbox/node-sqlite3', 'mafintosh/mongojs', 'tornadoweb/tornado', 'gevent/gevent',
  #   'percolatestudio/meteor-migrations', 'Polymer/polymer', 'Automattic/mongoose',
  #   'nodejs/node', 'sequelize/sequelize', 'Automattic/monk', 'balderdashy/waterline',
  #   'balderdashy/sails', 'playframework/playframework', 'pyinvoke/invoke',
  #   'msanders/snipmate.vim',

  #   # libs that have given me trouble
  #   'sindresorhus/atom-jshint', 'angular-ui-tree/angular-ui-tree',
  #   'boto/boto', 'rupa/z', 'lsegal/atom-runner'
  # ])
