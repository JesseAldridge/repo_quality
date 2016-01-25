# -*- coding: utf-8 -*-
import re, json, os, time

import requests

import config, calc_score
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

def write_repo(repo_dict, repo_path=None):
  if isinstance(repo_dict, basestring):
    repo_dict = json.loads(repo_dict)
  path = repo_path if repo_path else repo_dict['full_name']
  validate_path(path)
  cache_file_path = os.path.join(config.cache_dir_path, path.replace('/', '_')) + '.txt'
  if 'created_at' not in repo_dict:
    raise BadRepoException()
  print 'writing repo:', cache_file_path
  with open(cache_file_path, 'w') as f:
    f.write(json.dumps(repo_dict, indent=2))
  return cache_file_path

def get_mean_stars_per_issue():
  print 'getting mean_stars_per_issue'
  resp = requests.get(
    'https://repo-quality.firebaseio.com/mean_stars_per_issue.json?auth=' +
    secrets.firebase_token)
  try:
    mean_stars_per_issue = json.loads(resp.content)
  except Exception as e:
    print 'error loading mean_stars_per_issue:', e
    mean_stars_per_issue = 10
  return mean_stars_per_issue

def rate_repo(repo_dict, mean_stars_per_issue):
  score = calc_score.calc_score(repo_dict, mean_stars_per_issue)
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
    main_resp = requests.get('https://api.github.com/repos/twbs/bootstrap')
    cache_file_path = write_repo(main_resp.content)
    mod_time = os.path.getmtime(cache_file_path)
    assert time.time() - mod_time < 1, time.time() - mod_time
    mean_stars_per_issue = get_mean_stars_per_issue()
    rate_repo(calc_score.fake_repo_dict, mean_stars_per_issue)
    assert calc_score.fake_repo_dict['explanation']
  test()
