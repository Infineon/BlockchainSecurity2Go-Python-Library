import sys
import json
import argparse

from blocksec2go import open_pyscard, CardError
from blocksec2go import select_app, verify_pin, encrypted_keyimport
from blocksec2go.util import bytes_from_hex

def _encrypted_keyimport(args):
    reader = open_pyscard(args.reader)
    select_app(reader)
    if args.pin is not None:
        verify_pin(reader, args.pin)
    encrypted_keyimport(reader, args.seed)

    if args.machine_readable:
        json.dump({'status': 'success'}, fp=sys.stdout)
    else:
        print('OK - import succeeded')

def add_subcommand(subparsers):
    parser = subparsers.add_parser('encrypted_keyimport', description='Create a reproducible key from a given seed')
    parser.set_defaults(func=_encrypted_keyimport)
    parser.add_argument('seed', help='seed used to generate key', type=bytes_from_hex(16))
    parser.add_argument('--pin', help='PIN to use')