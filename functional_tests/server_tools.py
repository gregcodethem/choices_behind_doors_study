from fabric.api import run
from fabric.context_managers import (
    settings,
    shell_env,
)
from env_host import USERNAME_ON_HOST


def _get_manage_dot_py(host):
    return f'~/{host}/env/bin/python ~/{host}/manage.py'

def reset_database(username_on_host, host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{username_on_host}@{host}'):
        run(f'{manage_dot_py} flush --noinput')

def _get_server_env_vars(host):
    env_lines = run(f'cat ~/{host}/.env').splitlines()
    return dict(l.split('=') for l in env_lines if l)

def create_session_on_server(host, user_identifier, size):
    manage_dot_py = _get_manage_dot_py(host)
    # need to refactor so this is hidden:
    username_on_host = USERNAME_ON_HOST
    with settings(host_string=f'{username_on_host}@{host}'):
        env_vars = _get_server_env_vars(host)
    with shell_env(**env_vars):
        session_key = run(f'{manage_dot_py} create_session {user_identifier}')
    return session_key.strip()