"""Git worker"""

import sys
import subprocess
import os

GITIGNORE_FILE = '.gitignore'


def get_indexed_files():
    return subprocess.check_output(
        "git ls-files",
        shell=True).decode(sys.stdout.encoding).splitlines()


def add_to_gitignore(gitignore_file=None, *filenames):
    if gitignore_file is None:
        gitignore_file = GITIGNORE_FILE

    additional_filenames = []

    mod = 'r+' if gitignore_file in os.listdir() else 'w+'
    with open(gitignore_file, mod) as file:
        text_ignored_filenames = file.read()
        ignored_filenames = [line.strip() for line
                             in text_ignored_filenames.split('\n')]

        for filename in filenames:
            if filename not in ignored_filenames:
                additional_filenames.append(filename)

        if additional_filenames:
            text_to_add = '' if text_ignored_filenames.endswith('\n') else '\n'
            text_to_add += '\n'.join(additional_filenames) + '\n'
            file.write(text_to_add)


def _add_to_gitignore():
    with open('.gitignore', 'a+') as file:
        if 'beag.cfg' not in [line.strip() for line in file.readlines()]:
            gitignore_text = file.read()
            gitignore_text += '' if gitignore_text.endswith('\n') else '\n'
            file.write(gitignore_text + f'{"beag.cfg"}\n')


def is_file_indexed(filename):
    return filename in get_indexed_files()
