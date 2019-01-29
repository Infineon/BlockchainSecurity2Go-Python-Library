import sys
import json
import argparse

from blockchain2go.comm import open_pyscard, CardError
from blockchain2go.commands import select_app, get_key_info

def _get_key_info(args):
    reader = open_pyscard(args.reader)
    select_app(reader)
    (global_counter, counter, key) = get_key_info(reader, args.key_id)

    if args.machine_readable:
        json.dump({
            'status': 'success',
            'key_id': args.key_id,
            'global_counter': global_counter,
            'counter': counter,
            'key': key.hex()}, fp=sys.stdout)
    else:
        print('Remaining Signatures with card: {}'.format(global_counter))
        print('Remaining signatures with key {}: {}'.format(args.key_id, counter))
        print('Key (hex, encoded according to SEC1): ' + key.hex())

def add_subcommand(subparsers):
    parser = subparsers.add_parser('get_key_info', description='Get public key and counters')
    parser.set_defaults(func=_get_key_info)
    parser.add_argument('key_id', help='ID of the key to use', type=int)
