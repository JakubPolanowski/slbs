from slbs import path, SETTINGS
from slbs.sign.windows import sign_file


def sign_installer_windows():
    installer = path('target/${installer}')
    sign_file(installer, SETTINGS['app_name'] + ' Setup', SETTINGS['url'])
