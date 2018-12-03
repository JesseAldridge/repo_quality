import glob, os, json, time, sys
from datetime import datetime

import config, _2_repo_quality

debug = (len(sys.argv) > 1 and sys.argv[1] == '1')
print 'debug:', debug, sys.argv

print 'Running, {}'.format(str(datetime.now()))

repo_paths = []
cache_paths = glob.glob(os.path.join(config.cache_dir_path, '*.txt'))
# cache_paths = glob.glob(os.path.join(config.cache_dir_path, 'hapijs_hapi.txt'))
if debug:
  cache_paths = cache_paths[:3]
for cache_file_path in sorted(cache_paths):
  with open(cache_file_path) as f:
    try:
      repo_dict = json.loads(f.read())
    except Exception as e:
      print 'error reading {}: {}'.format(config.cache_dir_path, e)
      continue
  repo_paths.append(repo_dict['full_name'])
_2_repo_quality.pull_paths(repo_paths, ignore_cache=True)
