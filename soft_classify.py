import glob, os, json

import guesslanguage

import soft_train, config

paths = []
for cache_file_path in glob.glob(os.path.join(config.cache_dir_path, '*.txt')):
  with open(cache_file_path) as f:
    repo_dict = json.loads(f.read())
  paths.append(repo_dict['full_name'])

software, non_software = soft_train.classify(paths)

for path in software:
  print path
print '----'
for path in non_software:
  print path
