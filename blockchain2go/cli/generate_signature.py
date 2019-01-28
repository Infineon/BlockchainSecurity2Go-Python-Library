import sys
import json
import argparse

from blockchain2go.comm import open_pyscard, CardError
from blockchain2go.commands import select, verify_pin, generate_signature
from blockchain2go.util import bytes_from_hex

def _generate_signature(args):
  reader = open_pyscard(args.reader)
  select(reader)
  if args.pin is not None:
    verify_pin(reader, args.pin)
  (global_counter, counter, signature) = generate_signature(reader, args.key_id, args.hash)

  if args.machine_readable:
    json.dump({
      'status': 'success',
      'global_counter': global_counter,
      'counter': counter,
      'signature': signature.hex()}, fp=sys.stdout)
  else:
    print('Remaining Signatures with card: {}'.format(global_counter))
    print('Remaining signatures with key {}: {}'.format(args.key_id, counter))
    print('Signature (hex): ' + signature.hex())

def add_subcommand(subparsers):
  parser = subparsers.add_parser('generate_signature', description='Sign a hash with specified key')
  parser.set_defaults(func=_generate_signature)
  parser.add_argument('key_id', help='key id', type=int)
  parser.add_argument('hash', help='hash to sign, in hex', type=bytes_from_hex(32))
  parser.add_argument('--pin', help='PIN to use')