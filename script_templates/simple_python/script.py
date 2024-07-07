#!/usr/bin/env python3

import argparse
import logging

"""This is a script that does a thing."""

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

##########################
# DataClass example ######
##########################
#
# from dataclasses import dataclass
#
# @dataclass
# class MatchGroup:
#     group: str
#     regex: str

def main():
    argparser = argparse.ArgumentParser(description='My cool new script')
    argparser.add_argument('-m', '--multiplier', type=int, default=2, help='Multiplier (default: 2)')
    argparser.add_argument('number', type=int, help='Number to double')
    args = argparser.parse_args()

    prod = args.number * args.multiplier
    print(f'{args.number} * {args.multiplier} = {prod}')

if __name__=='__main__':
    main()