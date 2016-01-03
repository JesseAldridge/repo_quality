import os, json, datetime

import flask
from flask import request

import github_quality, config

app = flask.Flask(__name__)

app.jinja_env.variable_start_string='((('
app.jinja_env.variable_end_string=')))'
app.comment_start_string='((#'
app.comment_end_string='#))'

mean_stars_per_issue = github_quality.get_mean_stars_per_issue()

@app.route('/')
def index():
  print 'hello'
  res = flask.render_template('index.html')
  print 'rendered:', res
  return res

class DateTimeEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return (datetime.datetime.min + obj).time().isoformat()
    else:
      return super(DateTimeEncoder, self).default(obj)

@app.route('/<username>/<repo_name>')
def query_repo(username, repo_name):
  print 'request.args:', request.args
  repo = '/'.join((username, repo_name))
  repo_dict = github_quality.pull_repo(repo, mean_stars_per_issue, auth=config.auth_)

  with open(os.path.join(config.cache_dir_path, 'min_max.json')) as f:
    min_max = json.loads(f.read())
  # json_out = DateTimeEncoder().encode(repo_dict)
  filtered_dict = {k: repo_dict[k] for k in ('full_name', 'score', 'has_issues')}
  repo_json = json.dumps(filtered_dict)
  return flask.render_template(
    'main.html', repo_json=repo_json,
    min_score=min_max['min_score'], max_score=min_max['max_score'])

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 3000))
  app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', True))
