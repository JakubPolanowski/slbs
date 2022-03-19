from slbs import _server, SETTINGS, path
from slbs._aws import upload_file, upload_folder_contents
from slbs_runtime import slbsError
from slbs_runtime.platform import is_linux
from os.path import basename

import json

# TODO determine if this functionality should be removed given scope of slbs


def _upload_repo(username, password):
    status, response = _server.post_json('start_upload', {
        'username': username,
        'password': password
    })

    def unexpected_response(): return slbsError(
        'Received unexpected server response %d:\n%s' % (status, response)
    )
    if status // 2 != 100:
        raise unexpected_response()
    try:
        data = json.loads(response)
    except ValueError:
        raise unexpected_response()
    try:
        credentials = data['bucket'], data['key'], data['secret']
    except KeyError:
        raise unexpected_response()

    def dest_path(p): return username + '/' + SETTINGS['app_name'] + '/' + p
    installer = path('target/${installer}')
    installer_dest = dest_path(basename(installer))
    upload_file(installer, installer_dest, *credentials)
    uploaded = [installer_dest]
    if is_linux():
        repo_dest = dest_path(SETTINGS['repo_subdir'])
        uploaded.extend(
            upload_folder_contents(path('target/repo'),
                                   repo_dest, *credentials)
        )
        pubkey_dest = dest_path('public-key.gpg')
        upload_file(
            path('src/sign/linux/public-key.gpg'), pubkey_dest, *credentials
        )
        uploaded.append(pubkey_dest)
    status, response = _server.post_json('complete_upload', {
        'username': username,
        'password': password,
        'files': uploaded
    })
    if status != 201:
        raise unexpected_response()
