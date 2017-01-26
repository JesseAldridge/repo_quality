import json, os, re, getpass, glob, time, datetime, traceback

import requests, arrow, flask
from werkzeug import exceptions

from stuff import secrets
import config, repo_util, soft_train

if not os.path.exists(config.cache_dir_path):
  os.mkdir(config.cache_dir_path)

class g:
  search_reset_time = None

def pull_paths(paths, auth=config.auth_, ignore_cache=False):
  mean_stars_per_issue = repo_util.get_mean_stars_per_issue()
  repo_dicts = []
  min_score, max_score = None, None
  stars_per_issue_list = []
  for path in paths:
    try:
      repo_dict = pull_repo(path, mean_stars_per_issue, auth=auth, ignore_cache=ignore_cache)
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
      print (u'exception: {}; {}'.format(type(e).__name__, e.message)).encode('utf8')
      traceback.print_exc()

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

class PullFailed(Exception):
  pass

class FailedSeveralTimes(Exception):
  pass

search_api = SearchAPI()


def pull_repo_and_process(repo_path, mean_stars_per_issue, auth=None, ignore_cache=False):
  # If not in cache, pull_repo.

  repo_util.validate_path(repo_path)
  cache_file_path = os.path.join(config.cache_dir_path, repo_path.replace('/', '_') + '.txt')
  if not os.path.exists(cache_file_path) or ignore_cache:
    print 'pulling info:', cache_file_path
    pull_repo(repo_path)

  # Read repo from cache.

  with open(cache_file_path) as f:
    json_str = f.read()
  repo_dict = json.loads(json_str)

  # Set default values for keys I recently added to db (and therefore might be missing).

  repo_dict.setdefault('path', repo_path)
  if 'age' in repo_dict:
    repo_dict['age'] = datetime.timedelta(seconds=repo_dict['age'])
  else:
    repo_dict['age'] = arrow.now() - arrow.get(repo_dict['created_at'])
  if not 'score' in repo_dict:
    repo_util.rate_repo(repo_dict, mean_stars_per_issue)

  return repo_dict

def pull_repo(repo_path, mean_stars_per_issue, auth, ignore_cache=False):
  # Pull repo from GitHub and write to file.

  for _ in range(10):
    resp = requests.get('https://api.github.com/repos/' + repo_path, auth=auth)
    if resp.status_code == 200:
      print 'main xrate-limit-remaining:', resp.headers['x-ratelimit-remaining']
      repo_dict = json.loads(resp.content)
      repo_owner = repo_dict['owner']['login']
      owner_issue_count = pull_owner_issue_count(repo_path, repo_owner)
      repo_dict['repoq'] = {'owner_issue_count': owner_issue_count}
      repo_util.write_repo(repo_dict, mean_stars_per_issue, repo_path)
      break
    elif resp.status_code == 404:
      raise exceptions.NotFound()
    elif resp.status_code == 403:
      reset_time = resp.headers['X-RateLimit-Reset']
      print 'rate limit exceeded, sleeping for 60 seconds, reset_time:', reset_time
      time.sleep(60)
    else:
      print 'pull failed:', resp.status_code
      print '  resp:', resp.content[:100]
      raise PullFailed()
  else:
    raise FailedSeveralTimes()

def pull_owner_issue_count(repo_path, repo_owner):
  for _ in range(10):
    url = 'https://api.github.com/search/issues?q=repo:{}+author:{}'.format(repo_path, repo_owner)
    resp = requests.get(url, auth=auth)
    if resp.status_code == 200:
      return resp.content['total_count']
    elif resp.status_code == 403:
      reset_time = resp.headers['X-RateLimit-Reset']
      print 'rate limit exceeded, sleeping for 60 seconds, reset_time:', reset_time
      time.sleep(60)
    else:
      print 'pull failed:', resp.status_code
      print '  resp:', resp.content[:100]
      raise PullFailed()
  else:
    raise FailedSeveralTimes()



if __name__ == '__main__':
  paths = []
  for cache_file_path in glob.glob(os.path.join(config.cache_dir_path, '*.txt')):
    with open(cache_file_path) as f:
      repo_dict = json.loads(f.read())
    paths.append(repo_dict['full_name'])
  pull_paths(paths, auth=None, ignore_cache=True)


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
