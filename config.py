import os

from requests import auth

import secrets

cache_dir_path_unexpanded = '~/.github_quality'
cache_dir_path = os.path.expanduser(cache_dir_path_unexpanded)
use_auth = True
auth_ = auth.HTTPBasicAuth('JesseAldridge', secrets.github_api_key) if use_auth else None

if __name__ == "__main__":
  print cache_dir_path
  print auth_
