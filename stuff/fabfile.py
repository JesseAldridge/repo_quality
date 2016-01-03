import os

from fabric import api

env = api.env

proj_path = os.path.dirname(os.path.dirname(__file__))
proj_name = os.path.basename(proj_path)

env.user = 'ubuntu'
env.hosts = ['54.172.109.248']

@api.task
def deploy_server():
  api.local('rsync --exclude=".git" --exclude="junk" -v -r {0} {1}@{2}:~'.format(
    proj_path, env.user, env.hosts[0]))
  api.sudo('pkill -HUP gunicorn')

# def download_db():
#     api.local(
#         ('scp ubuntu@{host}:'
#          '~/{proj_name}/stuff/db.json remote_db.json').format(
#             host=env.hosts[0], proj_name=proj_name))
