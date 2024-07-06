#!/bin/sh
"exec" "$(dirname $(readlink -f $0))/venv/bin/python3" "$0" "$@"

import argparse
import logging
from proj import helpers

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

def main(args):
    """Main function"""
    prod = helpers.multiplier(args.number, args.multiplier)
    logger.info(f'{args.number} * {args.multiplier} = {prod}')

if __name__=='__main__':
    argparser = argparse.ArgumentParser(description='My cool new script')
    argparser.add_argument('-m', '--multiplier', type=int, default=2, help='Multiplier (default: 2)')
    argparser.add_argument('number', type=int, help='Number to double')
    argparse_args = argparser.parse_args()
    main(argparse_args)
