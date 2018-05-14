# -*- coding: utf-8 -*-
import re, json, os, time

import requests, arrow

import config, _0_calc_score
from stuff import secrets

class IllegalCharException(Exception):
  pass

class PathLengthException(Exception):
  pass

class BadRepoException(Exception):
  pass

def validate_path(path):
  if not re.match('[A-Za-z0-9_/-]+', path):
    raise IllegalCharException()
  if len(path) > 100:
    raise PathLengthException()

def write_repo(repo_dict, mean_stars_per_issue, repo_path=None):
  if isinstance(repo_dict, basestring):
    repo_dict = json.loads(repo_dict)
  path = repo_path if repo_path else repo_dict['full_name']
  validate_path(path)
  cache_file_path = os.path.join(config.cache_dir_path, path.replace('/', '_')) + '.txt'
  if 'created_at' not in repo_dict:
    raise BadRepoException()

  if os.path.exists(cache_file_path):
    with open(cache_file_path) as f:
      old_text = f.read()
    old_repo_dict = json.loads(old_text)
    repo_dict['timestamp_to_score'] = old_repo_dict.get('timestamp_to_score') or {}

  repo_dict['path'] = path
  repo_dict['age'] = (arrow.now() - arrow.get(repo_dict['created_at']))
  rate_repo(repo_dict, mean_stars_per_issue)
  now = arrow.utcnow()

  repo_dict.setdefault('timestamp_to_score', {})
  repo_dict['timestamp_to_score'][now.isoformat()] = repo_dict['score']
  repo_dict['age'] = repo_dict['age'].total_seconds()

  json_str = json.dumps(repo_dict, indent=2)
  print 'writing repo:', cache_file_path
  with open(cache_file_path, 'w') as f:
    f.write(json_str)
  return cache_file_path

def get_mean_stars_per_issue():
  # print 'getting mean_stars_per_issue'
  # resp = requests.get(
  #   'https://repo-quality.firebaseio.com/mean_stars_per_issue.json?auth=' +
  #   secrets.firebase_token)
  # try:
  #   mean_stars_per_issue = json.loads(resp.content)
  # except Exception as e:
  #   print 'error loading mean_stars_per_issue:', e
  #   mean_stars_per_issue = 10
  # return mean_stars_per_issue

  return 10

def rate_repo(repo_dict, mean_stars_per_issue):
  score = _0_calc_score.calc_score(repo_dict, mean_stars_per_issue)
  rating, explanation = score_to_rating(score)
  rating_str = ''
  for i in range(rating):
    rating_str += u'⭐️' + u' '
  if rating_str == '':
    rating_str = u'💩'
  repo_dict['rating_str'] = rating_str
  repo_dict['explanation'] = explanation

def score_to_rating(score):
  if score > 4000:
    return 5, 'LEGENDARY'
  elif score > 1000:
    return 4, 'Excellent'
  elif score > 400:
    return 3, 'Good'
  elif score > 200:
    return 2, 'Ok'
  elif score > 100:
    return 1, 'Bad'
  return 0, ''

if __name__ == '__main__':
  def test():
    # Test write_repo and get_mean_stars_per_issue
    main_resp = requests.get('https://api.github.com/repos/expressjs/express')
    mean_stars_per_issue = get_mean_stars_per_issue()
    repo_dict = json.loads(main_resp.content)
    pulls_resp = requests.get('https://api.github.com/repos/expressjs/express/pulls')
    repo_dict['pull_count'] = len(json.loads(pulls_resp.content))
    cache_file_path = write_repo(repo_dict, mean_stars_per_issue)

    mod_time = os.path.getmtime(cache_file_path)
    # assert time.time() - mod_time < 1, time.time() - mod_time
    print 'mean_stars_per_issue:', mean_stars_per_issue
    rate_repo(_0_calc_score.fake_repo_dict, mean_stars_per_issue)
    assert _0_calc_score.fake_repo_dict['explanation']
  test()
