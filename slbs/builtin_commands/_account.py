from slbs import path, _server
from slbs.builtin_commands import prompt_for_value, require_existing_project
from slbs.builtin_commands._util import update_json, SECRET_JSON
from slbs.cmdline import command

import logging

_LOG = logging.getLogger(__name__)

# TODO this should be removed, online repo not part of slbs scope


@command
def register():
    """
    Create an account for uploading your files
    """
    require_existing_project()
    username = prompt_for_value('Username')
    email = prompt_for_value('Real email')
    password = prompt_for_value('Password', password=True)
    print('')
    status, text = _server.post_json('register', {
        'username': username, 'email': email, 'password': password
    })
    if status == 201:
        if text:
            _LOG.info(text)
        _login(username, password)
    else:
        _LOG.error('Could not register:\n' + text)


@command
def login():
    """
    Save your account details to secret.json
    """
    require_existing_project()
    username = prompt_for_value('Username')
    password = prompt_for_value('Password', password=True)
    print('')
    _login(username, password)


def _login(username, password):
    update_json(path(SECRET_JSON), {
                'slbs_user': username, 'slbs_pass': password})
    _LOG.info('Saved your username and password to %s.', SECRET_JSON)
