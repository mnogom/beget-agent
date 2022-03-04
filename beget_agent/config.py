"""Config."""

import os
from dotenv import load_dotenv

PIPE_FILE = 'beag_pipe'

load_dotenv()


class Config:
    def __init__(self, host, port, username, password, remote_home):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.remote_home = remote_home


def read_config():
    return Config(host=os.getenv('SFTP_HOST'),
                  port=int(os.getenv('SFTP_PORT')),
                  username=os.getenv('SFTP_USERNAME'),
                  password=os.getenv('SFTP_PASSWORD'),
                  remote_home=os.getenv('SFTP_REMOTE_HOME'))


def read_beag_pipe():
    with open(PIPE_FILE, 'r') as file:
        return ';'.join(line.strip() for line in file.readlines() if line)
