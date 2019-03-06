import sys
import json
import argparse

import smartcard.System

def _list_readers(args):
    readers = smartcard.System.readers()
    if args.machine_readable:

        json.dump({'status': 'success', 'readers': [str(reader) for reader in readers]}, sys.stdout)
    else:
        for reader in readers:
            print(reader)

def add_subcommand(subparsers):
    parser = subparsers.add_parser('list_readers', description='List PC/SC readers connected to the system')
    parser.set_defaults(func=_list_readers)
