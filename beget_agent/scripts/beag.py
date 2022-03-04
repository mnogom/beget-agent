#!/usr/bin/env python3

"""Entry point."""
import sys

from beget_agent.cli import parse_args, COMMAND_PUT, COMMAND_RESTART, COMMAND_EXECUTE_PIPE
from beget_agent.commands import restart, put_files, execute_pipe
from beget_agent.exceptions import BAFileNotFoundError, BANeedRecursiveModException


def main():
    args = parse_args()

    if args['command'] == COMMAND_RESTART:
        restart()

    if args['command'] == COMMAND_PUT:
        try:
            put_files(files=args.get('files'),
                      recursive=args.get('recursive'),
                      intersection_to_index=args.get('intersection'),
                      all_files=args.get('all_files'))
        except BANeedRecursiveModException as exception:
            print(str(exception))
            sys.exit(1)

    if args['command'] == COMMAND_EXECUTE_PIPE:
        try:
            execute_pipe()
        except BAFileNotFoundError as exception:
            print(str(exception))
            sys.exit(1)





if __name__ == '__main__':
    main()
