import os

import paramiko
import time

from beget_agent.config import read_config, read_beag_pipe


def _command(command: str, encoding='utf-8'):
    return f'{command}\r\n'.encode(encoding)


def _sleeping_pipe(shell, *commands_parameters, sleep_time=1.0):
    for func, args in commands_parameters:
        func(args)
        time.sleep(sleep_time)


def ssh_command(func):
    def inner(*args, **kwargs):
        config = read_config()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=config.host,
                       port=config.port,
                       username=config.username,
                       password=config.password)

        shell = client.invoke_shell()

        kwargs['shell'] = shell
        kwargs['remote_home'] = config.remote_home
        kwargs['password'] = config.password
        output = func(*args, **kwargs)

        shell.close()
        client.close()
        return output

    return inner


@ssh_command
def execute_commands(command_sequence, **kwargs):
    _shell = kwargs.get('shell')
    _remote_home = kwargs.get('remote_home')
    _password = kwargs.get('password')

    _sleeping_pipe(
        _shell,
        (_shell.send, _command(f'ssh localhost -p 222')),
        (_shell.send, _command(f'{_password}')),
        (_shell.send, _command(f'cd {_remote_home}')),
        (_shell.send, _command(command_sequence))
    )

    print(_shell.recv(1024).decode('utf-8'))


def main():
    command_sequence = read_beag_pipe()
    print(command_sequence)
    execute_commands(command_sequence)


if __name__ == '__main__':
    main()
