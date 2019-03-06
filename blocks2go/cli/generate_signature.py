import sys
import json
import argparse

from blocks2go.comm import open_pyscard, CardError
from blocks2go.commands import select_app, verify_pin, generate_signature
from blocks2go.util import bytes_from_hex

def _generate_signature(args):
    reader = open_pyscard(args.reader)
    select_app(reader)
    if args.pin is not None:
        verify_pin(reader, args.pin)
    if len(args.hash) is not 64:
        raise RuntimeError('Invalid hash length')

    (global_counter, counter, signature) = generate_signature(reader, args.key_id, bytes.fromhex(args.hash))

    if args.machine_readable:
        json.dump({
            'status': 'success',
            'global_counter': global_counter,
            'counter': counter,
            'signature': signature.hex()}, fp=sys.stdout)
    else:
        print('Remaining signatures with card: {}'.format(global_counter))
        print('Remaining signatures with key {}: {}'.format(args.key_id, counter))
        print('Signature (hex): ' + signature.hex())

def add_subcommand(subparsers):
    parser = subparsers.add_parser('generate_signature', description='Sign a hash with specified key')
    parser.set_defaults(func=_generate_signature)
    parser.add_argument('key_id', help='key id', type=int)
    parser.add_argument('hash', help='hash to sign, in hex', type=str)
    parser.add_argument('--pin', help='PIN to use')