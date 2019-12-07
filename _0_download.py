import os, subprocess, shutil

import config

download_dir_path = os.path.expanduser('~/repoq-downloads')
if os.path.exists(download_dir_path):
  assert len(download_dir_path) > 5
  shutil.rmtree(download_dir_path)
  os.mkdir(download_dir_path)

def download_repo(repo_url_path):
  repo_file_name = repo_url_path.replace('/', '_') + '.txt'
  repo_file_path = os.path.join(config.cache_dir_path_unexpanded, repo_file_name)

  subprocess.call([
    'scp', 
    'repo_quality:{}'.format(repo_file_path), 
    os.path.join(download_dir_path, repo_file_name),
  ])
  

with open('_0_to_download.txt') as f:
  text = f.read()
for line in text.splitlines():
  download_repo(line)
