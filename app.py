import os, json, datetime, sys, traceback

import flask
from flask import request
from werkzeug import exceptions

import _2_repo_quality
import config
import _1_repo_util
import _0_repo_lists

app = flask.Flask(__name__)

app.jinja_env.variable_start_string = '((('
app.jinja_env.variable_end_string = ')))'
app.comment_start_string = '((#'
app.comment_end_string = '#))'

mean_stars_per_issue = _1_repo_util.get_mean_stars_per_issue()


@app.route('/')
def index():
  repo_lists = _0_repo_lists.repo_lists
  print 'list count:', len(repo_lists)
  return flask.render_template('index.html', repo_lists=repo_lists)


def get_repo(repo_path):
  repo_dict = _2_repo_quality.pull_repo(repo_path, mean_stars_per_issue, auth=config.auth_)
  whitelisted_dict = {
    k: repo_dict[k] for k in (
      'full_name', 'score', 'has_issues', 'rating_str', 'explanation',
      'stargazers_count', 'age', 'closed_issues', 'timestamp_to_score')
      if k in repo_dict
  }
  whitelisted_dict['issue_count'] = (
    repo_dict['open_issues'] -
    repo_dict.get('pull_count', 0) -
    repo_dict.get('self_issue_count', 0)
  )

  return whitelisted_dict


class DateTimeEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return obj.days
    else:
      return super(DateTimeEncoder, self).default(obj)


@app.route('/templates/<path:path>')
def send_js(path):
  return flask.send_from_directory('templates', path)


@app.route('/<username>/<repo_name>')
@app.route('/<username>/<repo_name>/')
def query_repo(username, repo_name):
  repo_dict = get_repo('/'.join((username, repo_name)))
  repo_json = DateTimeEncoder().encode(repo_dict)
  return flask.render_template('repo.html', repo_json=repo_json)


@app.route('/lists/<list_name>')
def query_list(list_name):
  repo_lists = _0_repo_lists.repo_lists
  paths = repo_lists[list_name] if list_name in repo_lists else None
  if paths:
    repos = []
    for path in paths:
      try:
        repos.append(get_repo(path))
      except Exception as e:
        print (u'exception: {}; {}'.format(type(e).__name__, e.message)).encode('utf8')
        traceback.print_exc()
    list_json = DateTimeEncoder().encode(sorted(repos, key=lambda r: -r['score']))
    return flask.render_template('list.html', list_json=list_json)
  abort(404)


if __name__ == '__main__':
  app.run(host='0.0.0.0')
