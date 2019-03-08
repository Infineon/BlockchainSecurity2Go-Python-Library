import sys
import json
import argparse

from blocksec2go import open_pyscard, CardError
from blocksec2go import select_app, change_pin

def _change_pin(args):
	reader = open_pyscard(args.reader)
	select_app(reader)
	puk = change_pin(reader, args.current_pin, args.new_pin)

	if args.machine_readable:
		json.dump({
			'status': 'success',
			'puk': puk.hex()}, fp=sys.stdout)
	else:
		print('New PUK to unlock card (hex): ' + puk.hex())

def add_subcommand(subparsers):
	parser = subparsers.add_parser('change_pin', description='Change the currently configured PIN')
	parser.set_defaults(func=_change_pin)
	parser.add_argument('current_pin', help='current PIN')
	parser.add_argument('new_pin', help='new PIN')