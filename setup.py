"""Create cross-platform desktop applications with Python and Qt

See:
https://github.com/JakubPolanowski/slbs  # TODO replace with new wiki once first release ready and wiki added
"""

from os.path import relpath, join
from setuptools import setup, find_packages

import os


def _get_package_data(pkg_dir, data_subdir):
    result = []
    for dirpath, _, filenames in os.walk(join(pkg_dir, data_subdir)):
        for filename in filenames:
            filepath = join(dirpath, filename)
            result.append(relpath(filepath, pkg_dir))
    return result


description = 'Create cross-platform desktop applications with Python and Qt'
setup(
    name='slbs',
    # Also update slbs/_defaults/requirements/base.txt when you change this:
    version='0.0.0',
    description=description,
    long_description=description + \
    '\n\nHome page: https://github.com/JakubPolanowski/slbs',
    author='Jakub Polanowski',
    author_email='jakubpol27@gmail.com',
    url='https://github.com/JakubPolanowski/slbs',
    packages=find_packages(exclude=('tests', 'tests.*')),
    package_data={
        'slbs': _get_package_data('fbs', '_defaults'),
        'slbs.builtin_commands':
            _get_package_data('slbs/builtin_commands', 'project_template'),
        'slbs.builtin_commands._gpg':  # TODO: check if this is required given goals of slbs
            ['Dockerfile', 'genkey.sh', 'gpg-agent.conf'],
        'slbs.installer.mac': _get_package_data(
            'slbs/installer/mac', 'create-dmg'
        )
    },
    # TODO: explore if version requirement appropriate
    install_requires=['PyInstaller>=3.4'],
    extras_require={
        # Also update requirements.txt when you change this:
        'licensing': ['rsa>=3.4.2'],  # TODO recheck if necessary
        'sentry': ['sentry-sdk>=0.6.6'],  # TODO recheck if necessary
        'upload': ['boto3']  # TODO recheck if necessary
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': ['slbs=slbs.__main__:_main']
    },
    license='GPLv3 or later',
    keywords='PyQt',
    platforms=['MacOS', 'Windows', 'Debian', 'Fedora', 'CentOS', 'Arch'],
    test_suite='tests'
)
