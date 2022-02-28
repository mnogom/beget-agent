#!/usr/bin/env python3

"""Entry point."""

from beget_agent.cli import parse_args, COMMAND_PUT, COMMAND_RESTART
from beget_agent.commands import restart, put_files


def main():
    args = parse_args()

    if args['command'] == COMMAND_RESTART:
        restart()

    if args['command'] == COMMAND_PUT:
        put_files(files=args.get('files'),
                  recursive=args.get('recursive'),
                  intersection_to_index=args.get('intersection'),
                  all_files=args.get('all_files'))


if __name__ == '__main__':
    main()
