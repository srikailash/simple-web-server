from araku import *

import argparse
import os
import sys
from araku import __version__ as version


def parse_args():
    parser = argparse.ArgumentParser(usage='''Araku <command> [project_directory] [options]
    list of commands:
        init            create initial project structure
        serve           run development server
        build           build project
    ''')
    parser.add_argument('command', choices=['init', 'build', 'version', 'serve'], help=argparse.SUPPRESS)
    parser.add_argument('project_directory', nargs='?', default=os.getcwd(),
                        help='directory which contains your config.py and content')
    #TODO: Add validator argument
    parser.add_argument('-p', '--port', type=int, default=8000, help='server port')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args.ports = args.port, args.port + 1
    args.debug = False
    return args


def build(args, output_dir=None):
    #TODO: Validator argument is not being taken currently for builder
    kwargs = {
        'validate': args.validate
    }

    if output_dir is not None:
        kwargs['output_dir'] = output_dir
    
    config = {
        'DEBUG': args.debug,
        'SERVER_PORT': args.ports[0],
        'NOTIFICATION_SERVER_PORT': args.ports[1],
    }
    #TODO: Implement Builder
    print("Buidling your text based blog")

def run(args):
    if args.command == 'init':
        #TODO: Implement project initializer
        #This is where a new project gets created
        print("########################################")
        print("Got a command to Initialise the project")
        print("To project_directory={0}, ports={1}".format(args.project_directory, args.port))
        print("########################################")
    elif args.command == 'build':
        #TODO: Implement Builder
        #Build step has to be done after updates to content
        print("########################################")
        print("Got a command to build")
        print("########################################")
    elif args.command == 'version':
        print("########################################")
        print(version)
        print("########################################")
    elif args.command == 'serve':
        args.debug = True
        #TODO: Implement server.py
        #Serve has to be done to start the server after building
        print("########################################")
        print("Got a command to serve blog that has already been generated")
        print("########################################")

def main():
    run(parse_args())
    print("Hello From Main after executing the command")


if __name__ == '__main__':
    main()