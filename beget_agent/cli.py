"""CLI parser."""

import argparse

COMMAND_PUT = 'put'
COMMAND_RESTART = 'restart'
COMMAND_EXECUTE_PIPE = 'execute_pipe'


def parse_args():
    parser = argparse.ArgumentParser(description='Beget SFTP agent')
    sub_parser = parser.add_subparsers(dest='command')

    _ = sub_parser.add_parser(name=COMMAND_RESTART,
                              help='Restart server. Store "./tmp/restart.txt"')

    _ = sub_parser.add_parser(name=COMMAND_EXECUTE_PIPE,
                              help='Execute file "beag_pipe"')

    put = sub_parser.add_parser(name=COMMAND_PUT,
                                help='Put files to server')
    put.add_argument(dest='files',
                     help='Files to store',
                     nargs='*')
    put.add_argument('-r',
                     help='Recursive upload. Use for directories',
                     action='store_true',
                     default=False)
    put.add_argument('-i',
                     help='Intersection with git index',
                     action='store_true',
                     default=False)
    put.add_argument('-a',
                     help='Put all files in current dir',
                     action='store_true',
                     default=False)

    args = parser.parse_args()

    if args.command == COMMAND_RESTART:
        return {'command': COMMAND_RESTART}
    if args.command == COMMAND_PUT:
        return {
            'command': COMMAND_PUT,
            'files': args.files,
            'recursive': args.r,
            'intersection': args.i,
            'all_files': args.a
        }
    if args.command == COMMAND_EXECUTE_PIPE:
        return {'command': COMMAND_EXECUTE_PIPE}
    parser.print_help()


if __name__ == '__main__':
    print(parse_args())
