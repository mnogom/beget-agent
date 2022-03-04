"""Core."""

import os

from paramiko import Transport, SFTPClient
from beget_agent.config import read_config
from progress.bar import PixelBar

FILE_TO_RESTART = 'tmp/restart.txt'


def _create_folders(file, _sftp, _remote_home):
    path, _ = os.path.split(file)
    dirs = path.split('/')
    for i, dir in enumerate(dirs):
        try:
            _sftp.mkdir(os.path.join(_remote_home, *dirs[:i + 1]))
        except OSError:
            pass


def sftp_command(func):
    def inner(*args, **kwargs):
        config = read_config()

        transport = Transport((config.host, config.port))
        transport.connect(username=config.username,
                          password=config.password)

        sftp = SFTPClient.from_transport(transport)

        kwargs['sftp'] = sftp
        kwargs['remote_home'] = config.remote_home
        output = func(*args, **kwargs)

        sftp.close()
        transport.close()
        return output
    return inner


@sftp_command
def store_files(local_files, **kwargs):
    _remote_home = kwargs.get('remote_home')
    _sftp = kwargs.get('sftp')

    for file in PixelBar('Uploading: ').iter(local_files):
        _create_folders(file, _sftp, _remote_home)
        remote_file = os.path.join(_remote_home, file)
        _sftp.put(file, remote_file)


@sftp_command
def store_restart(**kwargs):
    _remote_home = kwargs.get('remote_home')
    _sftp = kwargs.get('sftp')

    _create_folders(FILE_TO_RESTART, _sftp, _remote_home)
    _sftp.open(os.path.join(_remote_home, FILE_TO_RESTART), 'w')
