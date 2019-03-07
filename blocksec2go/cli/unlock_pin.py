import sys
import json
import argparse

from blocksec2go import open_pyscard, CardError
from blocksec2go import select_app, unlock_pin
from blocksec2go.util import bytes_from_hex

def _unlock_pin(args):
    reader = open_pyscard(args.reader)
    select_app(reader)
    unlock_pin(reader, args.puk)

    if args.machine_readable:
        json.dump({'status': 'success'}, fp=sys.stdout)
    else:
        print('OK - unlocked')

def add_subcommand(subparsers):
    parser = subparsers.add_parser('unlock_pin', description='Unlock a locked card')
    parser.set_defaults(func=_unlock_pin)
    parser.add_argument('puk', help='PUK to unlock card', type=bytes_from_hex())