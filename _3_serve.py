import os
import json
import datetime

import flask
from flask import request
from werkzeug import exceptions

import _2_repo_quality
import config
import _1_repo_util
from repo_lists import repo_lists

app = flask.Flask(__name__)

app.jinja_env.variable_start_string = '((('
app.jinja_env.variable_end_string = ')))'
app.comment_start_string = '((#'
app.comment_end_string = '#))'

mean_stars_per_issue = _1_repo_util.get_mean_stars_per_issue()


@app.route('/')
def index():
  print 'lists:', repo_lists
  return flask.render_template('index.html', repo_lists=repo_lists)


def get_repo(repo_path):
  repo_dict = _2_repo_quality.pull_repo(repo_path, mean_stars_per_issue, auth=config.auth_)
  whitelisted_dict = {
    k: repo_dict[k] for k in (
      'full_name', 'score', 'has_issues', 'rating_str', 'explanation',
      'stargazers_count', 'age', 'closed_issues', 'timestamp_to_score')
      if k in repo_dict
  }
  whitelisted_dict['issue_count'] = repo_dict['open_issues'] - repo_dict.get('pull_count', 0)
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
  paths = repo_lists[list_name] if list_name in repo_lists else None
  if paths:
    repos = []
    for path in paths:
      try:
        repos.append(get_repo(path))
      except exceptions.NotFound:
        pass
    list_json = DateTimeEncoder().encode(sorted(repos, key=lambda r: -r['score']))
    return flask.render_template('list.html', list_json=list_json)
  abort(404)


if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 3000))
  app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', True))
