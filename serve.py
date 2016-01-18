import os
import json
import datetime

import flask
from flask import request

import github_quality
import config
import l0_repo

app = flask.Flask(__name__)

app.jinja_env.variable_start_string = '((('
app.jinja_env.variable_end_string = ')))'
app.comment_start_string = '((#'
app.comment_end_string = '#))'

mean_stars_per_issue = l0_repo.get_mean_stars_per_issue()

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
        'nodejs/node',
        'senchalabs/connect',
        'hapijs/hapi'
    ],
    'front_end_frameworks': [
        'angular/angular',
        'facebook/react',
        'angular/angular.js',
        'jashkenas/backbone',
        'vuejs/vue',
        'jquery/jquery'
    ],
    'programming_languages': [
        'elixir-lang/elixir',
        'golang/go',
        'timburks/nu',
        'Microsoft/dotnet',
        'apple/swift',
        'ruby/ruby',
        'php/php-src',
        'dart-lang/sdk'
    ],
    'git_guis': [
        'pieter/gitx',
        'rowanj/gitx',
        'brotherbard/gitx',
        'laullon/gitx',
        'beheadedmyway/gity',
        'andreberg/gitx'
    ],
    'hundred_best': [
        'lodash/lodash',
        'jlmakes/scrollreveal.js',
        'carhartl/jquery-cookie',
        'qrohlf/trianglify',
        'tobiasahlin/SpinKit',
        'Alamofire/Alamofire',
        'jwagner/smartcrop.js',
        'roots/sage',
        'SnapKit/Masonry',
        'phanan/htaccess',
        'senchalabs/connect',
        'Famous/famous',
        'postcss/autoprefixer',
        'zenorocha/clipboard.js',
        'facebook/Shimmer',
        'sindresorhus/quick-look-plugins',
        'afaqurk/linux-dash',
        'twbs/bootstrap-sass',
        'daneden/animate.css',
        'briangonzalez/jquery.adaptive-backgrounds.js',
        'nodemailer/nodemailer',
        'zxing/zxing',
        'github/fetch',
        'wycats/handlebars.js',
        'PredictionIO/PredictionIO',
        'keen/dashboards',
        'fullstackio/FlappySwift',
        'douglascrockford/JSON-js',
        'NARKOZ/hacker-scripts',
        'vuejs/vue',
        'rackt/react-router',
        'IanLunn/Hover',
        'yeoman/yeoman',
        'FezVrasta/bootstrap-material-design',
        'Flipboard/FLEX',
        'scottjehl/picturefill',
        'greatfire/wiki',
        'hapijs/hapi',
        'HannahMitt/HomeMirror',
        'bevacqua/dragula',
        'facebook/pop',
        'phoenixframework/phoenix',
        'jquery/jquery',
        'petkaantonov/bluebird',
        'yudai/gotty',
        'gulpjs/gulp',
        'AFNetworking/AFNetworking',
        'sindresorhus/pageres',
        'jashkenas/backbone',
        'designmodo/Flat-UI',
        'plataformatec/devise',
        'Microsoft/dotnet',
        'onevcat/VVDocumenter-Xcode',
        'astaxie/build-web-application-with-golang',
        'facebook/flux',
        'resume/resume.github.com',
        'rbenv/rbenv',
        'sbstjn/timesheet.js',
        'h5bp/Effeckt.css',
        'google/web-starter-kit',
        'desandro/masonry',
        'mperham/sidekiq',
        'basecamp/trix',
        'harthur/brain',
        'go-martini/martini',
        'thoughtbot/bourbon',
        'dokku/dokku',
        'yaronn/blessed-contrib',
        'tpope/vim-pathogen',
        'ejci/favico.js',
        'wg/wrk',
        'square/retrofit',
        'balderdashy/sails',
        'google/iosched',
        'amazeui/amazeui',
        'jessepollak/card',
        'WickyNilliams/headroom.js',
        'caolan/async',
        'mailcheck/mailcheck',
        'enaqx/awesome-react',
        'facebook/osquery',
        'imakewebthings/waypoints',
        'purifycss/purifycss',
        'FreeCodeCamp/FreeCodeCamp',
        'typicode/json-server',
        'flightjs/flight',
        'marmelab/gremlins.js',
        'jashkenas/underscore',
        'joewalnes/websocketd',
        'rackt/redux',
        'postcss/postcss',
        'Thibaut/devdocs',
        'strongloop/express',
        'guzzle/guzzle',
        'nvbn/thefuck',
        'twbs/bootstrap',
        'limetext/lime',
        'koajs/koa',
        'davatron5000/FitText.js',
        'isagalaev/highlight.js'
    ]
}


@app.route('/')
def index():
    print 'lists:', repo_lists
    return flask.render_template('index.html', repo_lists=repo_lists)


def get_repo(repo_path):
    repo_dict = github_quality.pull_repo(repo_path, mean_stars_per_issue, auth=config.auth_)
    return {k: repo_dict[k] for k in (
        'full_name', 'score', 'has_issues', 'rating_str', 'explanation', 'open_issues',
        'stargazers_count', 'age', 'closed_issues') if k in repo_dict}


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
def query_repo(username, repo_name):
    repo_dict = get_repo('/'.join((username, repo_name)))
    repo_json = DateTimeEncoder().encode(repo_dict)
    return flask.render_template('repo.html', repo_json=repo_json)


@app.route('/lists/<list_name>')
def query_list(list_name):
    paths = repo_lists[list_name] if list_name in repo_lists else None
    if paths:
        list_json = DateTimeEncoder().encode(
            sorted([get_repo(path) for path in paths], key=lambda r: -r['score']))
        return flask.render_template('list.html', list_json=list_json)
    abort(404)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', True))
