"""Config."""

import os
from dotenv import load_dotenv

ENV_FILE = '.env'

load_dotenv()


def read_config():
    config = {'host': os.getenv('SFTP_HOST'),
              'port': int(os.getenv('SFTP_PORT')),
              'username': os.getenv('SFTP_USERNAME'),
              'password': os.getenv('SFTP_PASSWORD'),
              'remote_home': os.getenv('SFTP_REMOTE_HOME')}
    return config


def create_config(**kwargs):
    with open(ENV_FILE, 'w') as file:
        for key, value in kwargs.items():
            file.write(f'{key}={value}\n')


def is_config_exists():
    return ENV_FILE in os.listdir()
