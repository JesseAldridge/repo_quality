import os, subprocess, shutil, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import config

def download_repo(repo_url_path, missing_repos):
  repo_file_name = repo_url_path.replace('/', '_') + '.txt'
  repo_file_path = os.path.join(config.cache_dir_path_unexpanded, repo_file_name)

  cmd_arr = [
    'scp', 
    'repo_quality:{}'.format(repo_file_path), 
    os.path.join(download_dir_path, repo_file_name),
  ]
  proc = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  out_str = proc.communicate()[0]
  if 'No such file' in out_str:
    missing_repos.append(repo_url_path)  

def main():
  missing_repos = []
  download_dir_path = os.path.expanduser('~/repoq-downloads')
  if os.path.exists(download_dir_path):
    assert len(download_dir_path) > 5
    shutil.rmtree(download_dir_path)
    os.mkdir(download_dir_path)

  with open('_0_to_download.txt') as f:
    text = f.read()
  for line in text.splitlines():
    download_repo(line, missing_repos)
  print 'missing:', '\n'.join(missing_repos)

if __name__ == '__main__':
  main()
