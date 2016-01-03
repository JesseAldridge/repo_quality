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

def filtered_repo(repo_path):
  repo_dict = github_quality.pull_repo(repo_path, mean_stars_per_issue, auth=config.auth_)
  return {k: repo_dict[k] for k in ('full_name', 'score', 'has_issues')}


@app.route('/templates/<path:path>')
def send_js(path):
    return flask.send_from_directory('templates', path)

@app.route('/<username>/<repo_name>')
def query_repo(username, repo_name):
  repo_dict = filtered_repo('/'.join((username, repo_name)))
  repo_json = json.dumps(repo_dict)

  return flask.render_template('repo.html', repo_json=repo_json)

@app.route('/lists/<list_name>')
def query_list(list_name):
  paths = None
  if list_name == 'python_unit_testing':
    paths = [
      'rlisagor/freshen',
      'gabrielfalcao/sure',
      'gabrielfalcao/lettuce',
      'behave/behave',
      'nose-devs/nose2',
      'nose-devs/nose',
      'pytest-dev/pytest'
    ]
  elif list_name == 'web_frameworks':
    paths = [
      'meteor/meteor',
      'mitsuhiko/flask',
      'rails/rails',
      'django/django',
      'phoenixframework/phoenix',
      'balderdashy/sails',
      'strongloop/express',
      'nodejs/node'
    ]
  elif list_name == 'front_end_frameworks':
    paths = [
      'angular/angular',
      'facebook/react',
      'angular/angular.js',
      'jashkenas/backbone'
    ]
  elif list_name == 'programming_languages':
    paths = [
      'elixir-lang/elixir',
      'golang/go'
    ]
  if paths:
    list_json = json.dumps([filtered_repo(path) for path in paths])
    return flask.render_template('list.html', list_json=list_json)
  abort(404)


if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 3000))
  app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', True))
