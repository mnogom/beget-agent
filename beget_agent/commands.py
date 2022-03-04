"""Commands."""

import os

from beget_agent.sftp_client import store_restart, store_files
from beget_agent.ssh_client import execute_commands
from beget_agent.config import read_beag_pipe, PIPE_FILE
from beget_agent.exceptions import BANeedRecursiveModException, BAFileNotFoundError
from beget_agent.git import get_indexed_files


def restart():
    store_restart()


def _get_all_files(files):
    def inner(folder: str) -> list:
        plain_tree = []
        for root, directories, files in os.walk(folder):
            for file in files:
                plain_tree.append(os.path.join(root, file))
        return plain_tree

    full_list = []
    for node in files:
        if os.path.isfile(node):
            full_list.append(node)
        else:
            full_list.extend(inner(folder=node))
    return full_list


def put_files(files,
              recursive=False,
              intersection_to_index=False,
              all_files=False):
    if all_files:
        files = os.listdir()
    if any([os.path.isdir(file) for file in files]) and not recursive:
        raise BANeedRecursiveModException('You are trying to upload dir. '
                                          'Use -r flag')
    else:
        files = _get_all_files(files)
    if intersection_to_index:
        files = list(set(files).intersection(set(get_indexed_files())))
    store_files(files)


def execute_pipe():
    try:
        pipe_commands = read_beag_pipe()
    except FileNotFoundError:
        raise BAFileNotFoundError(f"Can't find file '{PIPE_FILE}'.")
    execute_commands(pipe_commands)
