import sys
import json
import argparse

from blockchain2go.comm import open_pyscard, CardError
from blockchain2go.commands import select, set_pin

def _set_pin(args):
  reader = open_pyscard(args.reader)
  select(reader)
  puk = set_pin(reader, args.pin)

  if args.machine_readable:
    json.dump({
      'status': 'success',
      'puk': puk.hex()}, fp=sys.stdout)
  else:
    print('PUK to unlock card (hex): ' + puk.hex())

def add_subcommand(subparsers):
  parser = subparsers.add_parser('set_pin', description='Configure a PIN')
  parser.set_defaults(func=_set_pin)
  parser.add_argument('pin', help='new PIN')