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

repo_lists = {
  'python_unit_testing': [
    'rlisagor/freshen',
    'gabrielfalcao/sure',
    'gabrielfalcao/lettuce',
    'behave/behave',
    'nose-devs/nose2',
    'nose-devs/nose',
    'pytest-dev/pytest'
  ],
  'web_frameworks': [
    'meteor/meteor',
    'mitsuhiko/flask',
    'rails/rails',
    'django/django',
    'phoenixframework/phoenix',
    'balderdashy/sails',
    'strongloop/express',
    'nodejs/node'
  ],
  'front_end_frameworks': [
    'angular/angular',
    'facebook/react',
    'angular/angular.js',
    'jashkenas/backbone'
  ],
  'programming_languages': [
    'elixir-lang/elixir',
    'golang/go',
    'timburks/nu',
  ],
  'git_guis': [
    'pieter/gitx',
    'rowanj/gitx',
    'brotherbard/gitx',
    'laullon/gitx',
    'beheadedmyway/gity',
    'andreberg/gitx'
  ]
}


@app.route('/')
def index():
  print 'lists:', repo_lists
  res = flask.render_template('index.html', repo_lists=repo_lists)
  print 'rendered:', res
  return res

def filtered_repo(repo_path):
  repo_dict = github_quality.pull_repo(repo_path, mean_stars_per_issue, auth=config.auth_)
  return {k: repo_dict[k] for k in (
    'full_name', 'score', 'has_issues', 'rating_str', 'explanation')}


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
  paths = repo_lists[list_name] if list_name in repo_lists else None
  if paths:
    list_json = json.dumps(
      sorted([filtered_repo(path) for path in paths], key=lambda r: -r['score']))
    return flask.render_template('list.html', list_json=list_json)
  abort(404)


if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 3000))
  app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', True))
