import glob, os, json, time

import config, github_quality

while True:
  paths = []
  for cache_file_path in glob.glob(os.path.join(config.cache_dir_path, '*.txt')):
    with open(cache_file_path) as f:
      try:
        repo_dict = json.loads(f.read())
      except Exception as e:
        print 'error reading {}: {}'.format(config.cache_dir_path), e
        continue
    paths.append(repo_dict['full_name'])
  github_quality.pull_paths(paths, ignore_cache=True)

  time.sleep(60 * 60 * 24)
