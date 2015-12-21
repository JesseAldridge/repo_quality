import os, json, datetime

import flask
from flask import request

import github_quality

app = flask.Flask(__name__)

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

@app.route('/check')
def render():
    repo = request.args.get('repo')
    res = github_quality.pull_repo(repo)

    print 'res:', res, type(res)
    json_out = DateTimeEncoder().encode(res)
    return flask.render_template('main.html', json_out=json_out)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=port==3000)
