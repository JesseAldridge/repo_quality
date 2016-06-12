import os

from fabric import api

env = api.env

proj_path = os.path.dirname(os.path.dirname(__file__))
proj_name = os.path.basename(proj_path)

env.user = 'ubuntu'
env.hosts = ['repo_quality']
env.use_ssh_config = True


@api.task
def deploy_server():
    api.local('rsync --exclude=".git" --exclude="junk" -v -r {0} {1}@{2}:~'.format(
        proj_path, env.user, env.hosts[0]))
    api.sudo('pkill -HUP gunicorn')
    # "Unable to resolve host" error is normal
    print 'now do:'
    print 'ssh repo_quality'
    print 'ps aux | grep update_cache'
    print 'sudo kill {pid}'
    print 'sudo python update_cache_loop.py &'
    print 'cmd+d to logoff'


@api.task
def fetch_log():
    log_path = os.path.join(proj_name, 'nohup.out')
    command = "rsync repo_quality:{} .".format(log_path)
    api.local(command)
    local_path = os.path.basename(log_path)
    api.local('tail -n 100 {}'.format(local_path))
    os.remove(local_path)
