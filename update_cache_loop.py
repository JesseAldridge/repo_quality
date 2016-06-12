import glob, os, json, time

import config, github_quality

debug = False



while True:
  repo_paths = []
  cache_paths = glob.glob(os.path.join(config.cache_dir_path, '*.txt'))
  if debug:
    cache_paths = cache_paths[:3]
  for cache_file_path in cache_paths:
    with open(cache_file_path) as f:
      try:
        repo_dict = json.loads(f.read())
      except Exception as e:
        print 'error reading {}: {}'.format(config.cache_dir_path, e)
        continue
    repo_paths.append(repo_dict['full_name'])
  github_quality.pull_paths(repo_paths, ignore_cache=True)

  if debug:
    time.sleep(1)
  else:
    time.sleep(60 * 60 * 24)
