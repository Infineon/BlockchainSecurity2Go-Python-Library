import sys
import json
import argparse

from blocksec2go import open_pyscard, CardError
from blocksec2go import select_app, generate_keypair

def _generate_keypair(args):
    reader = open_pyscard(args.reader)
    select_app(reader)
    key_id = generate_keypair(reader)

    if args.machine_readable:
        json.dump({'status': 'success', 'key_id': key_id}, fp=sys.stdout)
    else:
        print('Key ID: {}'.format(key_id))

def add_subcommand(subparsers):
    parser = subparsers.add_parser('generate_keypair', description='Generate a new keypair')
    parser.set_defaults(func=_generate_keypair)
