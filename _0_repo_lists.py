import collections

repo_lists = collections.OrderedDict([
    ('connect_middleware', [
        'aaronblohowiak/routes.js',
        'andrewrk/connect-multiparty',
        'andrewrk/connect-static',
        'cojs/co-body',
        'dominictarr/config-chain',
        'dominictarr/hyperscript',
        'expressjs/body-parser',
        'expressjs/compression',
        'expressjs/cookie-parser',
        'expressjs/cookie-session',
        'expressjs/csurf',
        'expressjs/errorhandler',
        'expressjs/keygrip',
        'expressjs/method-override',
        'expressjs/morgan',
        'expressjs/response-time',
        'expressjs/serve-favicon',
        'expressjs/serve-favicon',
        'expressjs/serve-index',
        'expressjs/serve-static',
        'expressjs/session',
        'expressjs/timeout',
        'expressjs/vhost',
        'ghostsnstuff/serve-file-download',
        'isaacbw/node-egress',
        'isaacs/redsess',
        'isaacs/st',
        'isaacs/st',
        'jed/cookies',
        'jed/keygrip',
        'ljharb/qs',
        'mafintosh/is-my-json-valid',
        'mikeal/filed',
        'mikeal/request',
        'mscdex/connect-busboy',
        'pillarjs/cookies',
        'Raynos/body',
        'Raynos/error',
        'Raynos/http-methods',
        'Raynos/npm-less',
        'Raynos/redirecter',
        'Raynos/routes-router',
        'Raynos/send-data',
        'Raynos/serve-browserify',
        'Raynos/static-config',
        'raynos/validate-form',
        'rvagg/bole',
        'rvagg/level-session',
        'rvagg/node-generic-session',
        'saambarati/mapleTree',
        'spumko/joi',
        'stream-utils/raw-body',
        'stream-utils/raw-body',
        'stream-utils/raw-body',
        'visionmedia/consolidate.js/',
    ]),
    ('databases', [
        'google/leveldb',
        'mongodb/mongo',
        'neo4j/neo4j',
        'antirez/redis',
        'rethinkdb/rethinkdb',
        'pouchdb/pouchdb',
        'thinkaurelius/titan',
    ]),
    ('deep_learning', [
        'tensorflow/tensorflow',
        'fchollet/keras',
        'BVLC/caffe',
        'dmlc/mxnet',
        'Theano/Theano',
        'Microsoft/CNTK',
        'deeplearning4j/deeplearning4j',
        'baidu/paddle',
        'pytorch/pytorch',
        'pfnet/chainer',
        'torch/torch7',
        'NVIDIA/DIGITS',
        'tflearn/tflearn',
        'caffe2/caffe2',
        'davisking/dlib',
    ]),
    ('front_end_frameworks', [
        'lhorie/mithril.js',
        'mui-org/material-ui',
        'Polymer/polymer',
        'reactjs/redux',
        'riot/riot',
        'stimulusjs/stimulus',
        'vuejs/vue',
    ]),
    ('git_guis', [
        'pieter/gitx',
        'rowanj/gitx',
        'brotherbard/gitx',
        'laullon/gitx',
        'beheadedmyway/gity',
        'andreberg/gitx'
    ]),
    ('graphing', [
      'd3/d3',
      'chartjs/Chart.js',
      'flot/flot',
    ]),
    ('hapi_plugins', [
        'franciscogouveia/hapi-rbac',
        'toymachiner62/hapi-authorization',
        'hapijs/bell',
        'codedoctor/hapi-auth-anonymous',
        'hapijs/hapi-auth-basic',
        'Salesflare/hapi-auth-bearer-simple',
        'johnbrett/hapi-auth-bearer-token',
        'hapijs/hapi-auth-cookie',
        'asafdav/hapi-auth-extra',
        'hapijs/hapi-auth-hawk',
        'ryanfitz/hapi-auth-jwt',
        '58bits/hapi-auth-signature',
        'molekilla/hapi-passport-saml',
        'Mkoopajr/hapi-session-mongo',
        'glennjones/hapi-swagger',
        'codeandfury/node-hapi-swagger-models',
        'z0mt3c/hapi-swaggered',
        'z0mt3c/hapi-swaggered-ui',
        'hapijs/lout',
        'codeva/hapi-i18n',
        'maxnachlinger/hapi-l10n-gettext',
        'gpierret/hapi18n',
        'opentable/hapi-accept-language',
        'ozum/hapi-locale',
        'Wayfarer247/airbrake-hapi',
        'danielb2/blipp',
        'hapijs/good',
        'mac-/hapi-statsd',
        'idosh/hapi-alive',
        'aduis/hapi-rabbit',
        'mtharrison/susie',
        'nlf/blankie',
        'hapijs/crumb',
        'btmorex/hapi-server-session',
        'hapijs/yar',
        'mikefrey/hapi-dust',
        'gergoerdosi/hapi-json-view',
        'landau/hapi-react',
        'jedireza/hapi-react-views',
        'tanepiper/quorra',
        'watchup/hapi-mongoose',
        'hapijs/bassmaster',
        'devinivy/bedwetter',
        'g-div/crudy',
        'devinivy/dogwater',
        'nathanbuchar/hapi-glee',
        'bleupen/halacious',
        'sigfox/hapi-algolia-search',
        'poeticninja/hapi-assets',
        'ide/hapi-async-handler',
        'lob/hapi-bookshelf-models',
        'lob/hapi-bookshelf-serializer',
        'brainsiq/hapi-boom-decorators',
        'poeticninja/hapi-cache-buster',
        'gergoerdosi/hapi-cloudinary-connector',
        'AdrieanKhisbe/configue',
        'knownasilya/hapi-decorators',
        'christophercliff/hapi-dropbox-webhooks',
        'briandela/hapi-heroku-helpers',
        'danielb2/hapi-info',
        'sibartlett/hapi-io',
        'maxnachlinger/hapi-level-db',
        'ruiquelhas/hapi-magic-filter',
        'gergoerdosi/hapi-mailer',
        'jedireza/hapi-mongo-models',
        'codedoctor/hapi-mongoose-db-connector',
        'poeticninja/hapi-named-routes',
        'Pranay92/hapi-next',
        'jedireza/hapi-node-postgres',
        'christophercliff/hapi-nudge',
        'caligone/hapio',
        'developmentseed/hapi-paginate',
        'fknop/hapi-pagination',
        'sandfox/node-hapi-redis',
        'developmentseed/hapi-response-meta',
        'clarkie/hapi-route-directory',
        'bsiddiqui/hapi-router',
        'codedoctor/hapi-routes-status',
        'codeandfury/node-hapi-sequelize',
        'danecando/hapi-sequelized',
        'viniciusbo/hapi-suricate',
        'mtharrison/hapi-to',
        'christophercliff/hapi-webpack',
        'atroo/hapi-webpack-dev-server-plugin',
        'mark-bradshaw/mrhorse',
        'dschenkelman/patova',
        'hapijs/poop',
        'hapijs/reptile',
        'walmartlabs/ridicule',
        'hapijs/scooter',
        'continuationlabs/tacky',
        'briandela/therealyou',
        'smaxwellstewart/toothache',
        'vdeturckheim/tournesol',
        'hapijs/tv',
        'cristobal151/hapi-recaptcha',
        'ruiquelhas/blaine',
        'ruiquelhas/burton',
        'ruiquelhas/copperfield',
        'ruiquelhas/coutts',
        'ruiquelhas/fischbacher',
        'ruiquelhas/henning',
        'ruiquelhas/houdin',
        'ruiquelhas/lafayette',
        'ruiquelhas/supervizor',
        'ruiquelhas/thurston',
        'mac-/ratify',
        'hapijs/boom',
        'hapijs/confidence',
        'hapijs/faketoe',
        'hapijs/glue',
        'hapijs/h2o2',
        'hapijs/hoek',
        'hapijs/inert',
        'hapijs/joi',
        'hapijs/kilt',
        'hapijs/lab',
        'hapijs/makemehapi',
        'hapijs/nes',
        'hapijs/qs',
        'hapijs/rejoice',
        'hapijs/shot',
        'hapijs/topo',
        'hapijs/vision',
        'hapijs/wreck'
    ]),
    ('hundred_best', [
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
    ]),
    ('node_sql', [
        'dresende/node-orm2',
        'tgriesser/bookshelf',
        'felixge/node-mysql',
        '1602/jugglingdb',
        'brianc/node-postgres',
        'tgriesser/knex',
        'balderdashy/waterline',
        'sequelize/sequelize',
        'devinivy/dogwater'
    ]),
    ('programming_languages', [
        'Microsoft/dotnet',
        'apple/swift',
        'rust-lang/rust',
        'golang/go',
        'jashkenas/coffeescript',
        'ruby/ruby',
        'php/php-src',
        'JuliaLang/julia',
        'elixir-lang/elixir',
        'scala/scala',
        'clojure/clojure',
        'dotnet/roslyn',
        'erlang/otp',
        'JetBrains/kotlin',
        'nim-lang/Nim',
        'elm-lang/elm-compiler',
        'purescript/purescript',
        'timburks/nu',
        'Frege/frege',
        'gkz/LiveScript',
        'stevedekorte/io',
        'groovy/groovy-core',
        'racket/racket',
        'HaxeFoundation/haxe',
        'D-Programming-Language/dmd',
        'fsharp/fsharp',
        'eholk/harlan',
        'red/red',
        'amber-smalltalk/amber',
        'ocaml/ocaml',
        'dart-lang/sdk',
        'dylan-lang/opendylan',
        'chapel-lang/chapel',
    ]),
    ('python_rpc', [
        'shibukawa/curl_as_dsl',
        'irmen/Pyro4',
        'tomerfiliba/rpyc',
        'arskom/spyne',
        'python-symmetric-jsonrpc',
        'dwb/jsonrpc2-zeromq-python',
        'kiorky/SOAPpy',
        'wamp-proto/wamp-proto',
        'geoffwatts/zmqrpc',
        '0rpc/zerorpc-python',
    ]),
    ('python_unit_testing', [
        'rlisagor/freshen',
        'gabrielfalcao/sure',
        'gabrielfalcao/lettuce',
        'behave/behave',
        'nose-devs/nose2',
        'nose-devs/nose',
        'pytest-dev/pytest'
    ]),
    ('redis_clients', [
        "antirez/redis-doc",
        "mikeheier/Redis-AS3",
        "crypt1d/redi.sh",
        "redis/hiredis",
        "toymachine/libredis",
        "ctstone/csredis",
        "mhowlett/Nhiredis",
        "migueldeicaza/redis-sharp",
        "andrew-bn/RedisBoost",
        "ServiceStack/ServiceStack.Redis",
        "StackExchange/StackExchange.Redis",
        "mrpi/redis-cplusplus-client",
        "shawn246/redis_client",
        "cylix/cpp_redis",
        "uglide/qredisclient",
        "zhengshuxin/acl",
        "luca3m/redis3m",
        "nekipelov/redisclient",
        "hmartiro/redox",
        "Levhav/SimpleRedisClient",
        "0xsky/xredis",
        "ptaoussanis/carmine",
        "vseloved/cl-redis",
        "stefanwille/crystal-redis",
        "adilbaig/Tiny-Redis",
        "dartist/redis_client",
        "himulawang/i_redis",
        "ra1u/redis-dart",
        "danieleteti/delphiredisclient",
        "artemeff/exredis",
        "whatyouhide/redix",
        "wooga/eredis",
        "adrienmo/eredis_cluster",
        "japerk/erldis",
        "jeremyong/sharded_eredis",
        "bakkdoor/redis.fy",
        "emacstheviking/gnuprolog-redisclient",
        "alphazero/Go-Redis",
        "go-redis/redis",
        "simonz05/godis",
        "keimoon/gore",
        "xuyu/goredis",
        "gosexy/redis",
        "mediocregopher/radix.v2",
        "garyburd/redigo",
        "hoisie/redis",
        "shipwire/redis",
        "tideland/golib/tree/master/redis",
        "tideland/golib",
        "informatikr/hedis",
        "vangberg/iodis",
        "xetorthio/jedis",
        "alphazero/jredis",
        "mp911de/lettuce",
        "vert-x/mod-redis",
        "spullara/redis-protocol",
        "caoxinyu/RedisClient",
        "mrniko/redisson",
        "e-mzungu/rjc",
        "h0x91b/fast-redis-cluster",
        "h0x91b/redis-fast-driver",
        "jkaye2012/redis.jl",
        "Zeroloop/lasso-redis",
        "daurnimator/lredis",
        "agladysh/lua-hiredis",
        "nrk/redis-lua",
        "markuman/go-redis",
        "matsumoto-r/mruby-redis",
        "nim-lang/Nim",
        "luin/ioredis",
        "NodeRedis/node_redis",
        "fictorial/redis-node-client",
        "rootslab/spade",
        "mjackson/then-redis",
        "thunks/thunk-redis",
        "lp/ObjCHiredis",
        "dizzus/RedisKit",
        "0xffea/ocaml-redis",
        "ik5/redis_client.fpc",
        "wjackson/AnyEvent-Hiredis",
        "miyagawa/AnyEvent-Redis",
        "iph0/AnyEvent-Redis-RipeRedis",
        "marcusramberg/mojo-redis",
        "PerlRedis/perl-redis",
        "smsonline/redis-cluster-perl",
        "shogo82148/Redis-Fast",
        "trinitum/RedisDB",
        "amphp/redis",
        "cheprasov/php-redis-client",
        "colinmollenhour/credis",
        "ziogas/PHP-Redis-implementation",
        "jamescauwelier/PSRedis",
        "phpredis/phpredis",
        "nrk/predis",
        "swoole/redis-async",
        "jdp/redisent",
        "Shumkov/Rediska",
        "yampee/Redis",
        "lp/puredis",
        "aio-libs/aioredis",
        "jonathanslenders/asyncio-redis",
        "evilkost/brukva",
        "aallamaa/desir",
        "brainix/pottery",
        "pepijndevos/pypredis",
        "schlitzered/pyredis",
        "andymccurdy/redis-py",
        "khamin/redisca2",
        "fiorix/txredisapi",
        "bwlewis/rredis",
        "eu90h/rackdis",
        "stchang/redis",
        "rebolek/prot-redis",
        "mloughran/em-hiredis",
        "madsimian/em-redis",
        "amakawa/redic",
        "redis/redis-rb",
        "AsoSunag/redis-client",
        "mitsuhiko/redis-rs",
        "mneumann/rust-redis",
        "chrisdinn/brando",
        "twitter/finagle",
        "andreyk0/redis-client-scala-netty",
        "etaty/rediscala",
        "chiradip/RedisClient",
        "debasishg/scala-redis",
        "acrosa/scala-redis",
        "top10/scala-redis-client",
        "Livestream/scredis",
        "pk11/sedis",
        "carld/redis-client.egg",
        "czechboy0/Redbird",
        "Farhaddc/Swidis",
        "ronp001/SwiftRedis",
        "rabc/ZRedis",
        "gahr/retcl",
        "antirez/redis",
        "hishamco/vRedis",
        "carlosabalde/libvmod-redis",
        "resque/resque",
        "nvie/rq",
        "ask/celery",
        "paulasmuth/fnordmetric",
        "soveran/ohm",
        "celery/kombu",
        "dahlia/sider",
        "hollodotme/readis",
        "nateware/redis-objects",
        "iamteem/redisco",
        "sripathikrishnan/redis-rdb-tools",
        "pconstr/rdb-parser",
        "pconstr/redis-sync",
        "soveran/ost",
        "antirez/redis-sampler",
        "paulasmuth/recommendify",
        "redis-store/redis-store",
        "steelThread/redmon",
        "FetLife/rollout",
        "nicolasff/webdis",
        "seatgeek/soulmate",
        "ryanlecompte/redis_failover",
        "delano/redis-dump",
        "sneakybeaky/mod_redis",
        "agoragames/leaderboard",
        "nrk/redis-rdb",
        "slact/lua-ohm",
        "chrisboulton/php-resque",
        "ErikDubbelboer/phpRedisAdmin",
        "stephpy/timeline-bundle",
        "lsbardel/python-stdnet",
        "bbangert/retools",
        "pconstr/recurrent",
        "agoragames/amico",
        "qi4j/qi4j-sdk",
        "spring-projects/spring-data-redis",
        "sasanrose/phpredmin",
        "bradvoth/redis-tcl",
        "uglide/RedisDesktopManager",
        "fastogt/fastoredis",
        "poying/redis-mount",
        "josiahcarlson/rpqueue",
        "josiahcarlson/rom",
        "adriano-di-giovanni/node-redis-keychain",
        "eugef/phpRedExpert",
        "hibernate/hibernate-ogm",
        "binarydud/pyres",
        "flygoast/Redis-RdbParser",
        "percolate/redset",
        "Redsmin/redsmin",
        "stephenmcd/hot-redis",
        "FGRibreau/redistree",
        "caio/Redis-NaiveBayes",
        "wingify/agentredrabbit",
        "redtrine/redtrine",
        "Redsmin/redis-lua-unit",
        "FGRibreau/node-redis-info",
        "FGRibreau/redis-tool",
        "cinience/RedisStudio",
        "no13bus/redispapa",
        "HangfireIO/Hangfire",
        "coleifer/huey",
        "coleifer/walrus",
        "jacket-code/redisPlatform",
        "ienaga/RedisPlugin",
        "maxbrieiev/promise-redis",
        "hedisdb/hedis",
        "pkulchenko/ZeroBranePackage",
        "antirez/redis-io"
    ]),
    ('vue_state', [
        'visionmedia/superagent',
        'vuejs/vuex',
        'reactjs/redux',
        'egoist/revue',
        'vuejs/vue-resource',
        'facebook/flux'
    ]),
    ('web_frameworks', [
        'koajs/koa',
        'go-martini/martini',
        'meteor/meteor',
        'mitsuhiko/flask',
        'rails/rails',
        'django/django',
        'phoenixframework/phoenix',
        'balderdashy/sails',
        'strongloop/express',
        'nodejs/node',
        'senchalabs/connect',
        'hapijs/hapi',
        'laravel/laravel',
        'symfony/symfony',
        'linnovate/mean',
        'revel/revel',
        'cakephp/cakephp',
        'derbyjs/derby',
        'padrino/padrino-framework',
        'hanami/hanami',
        'keithwhor/nodal',
        'kraih/mojo',
        'ninjaframework/ninja',
        'web2py/web2py',
        'pakyow/pakyow',
        'perl-catalyst/catalyst-runtime',
        'vapor/vapor',
    ]),
    ('wysiwyg', [
        'froala/wysiwyg-editor',
    ]),
])
