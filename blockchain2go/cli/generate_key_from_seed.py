import sys
import json
import argparse

from blockchain2go.comm import open_pyscard, CardError
from blockchain2go.commands import select_app, verify_pin, generate_key_from_seed
from blockchain2go.util import bytes_from_hex

def _generate_key_from_seed(args):
  reader = open_pyscard(args.reader)
  select_app(reader)
  if args.pin is not None:
    verify_pin(reader, args.pin)
  generate_key_from_seed(reader, args.seed)

  if args.machine_readable:
    json.dump({'status': 'success'}, fp=sys.stdout)
  else:
    print('OK - import succeeded')

def add_subcommand(subparsers):
  parser = subparsers.add_parser('generate_key_from_seed', description='Create a reproducible key from a given seed')
  parser.set_defaults(func=_generate_key_from_seed)
  parser.add_argument('seed', help='seed used to generate key', type=bytes_from_hex(16))
  parser.add_argument('--pin', help='PIN to use')