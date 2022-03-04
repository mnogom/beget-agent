import paramiko
import time

from beget_agent.config import read_config


def _command(command: str, encoding='utf-8'):
    return f'{command}\r\n'.encode(encoding)


def _sleeping_pipe(shell, *commands_parameters, sleep_time=1.0):
    for func, args in commands_parameters:
        func(args)
        print(shell.recv_ready())
        time.sleep(sleep_time)
        print(shell.recv_ready())


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
def execute_commands(command_list, **kwargs):
    _shell = kwargs.get('shell')
    _remote_home = kwargs.get('remote_home')
    _password = kwargs.get('password')

    _sleeping_pipe(
        _shell,
        (_shell.send, _command(f'ssh localhost -p 222')),
        (_shell.send, _command(f'{_password}')),
        (_shell.send, _command(f'cd {_remote_home}')),
        (_shell.exec_command, _command(command_list))
    )

    print(_shell.recv(1024).decode('utf-8'))


def main():
    import sshtunnel

    config = read_config()
    with sshtunnel.open_tunnel(
        (config.host, config.port),
        ssh_username=config.username,
        ssh_private_key_password=config.password,
        remote_bind_address=('localhost', 222)
    ) as tunnel:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('127.0.0.1', 10022)
        # do some operations with client session
        client.close()

    print('FINISH!')


if __name__ == '__main__':
    main()
