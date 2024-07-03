#!/usr/bin/env python3

import argparse

def main(args):
    prod = args.number * args.multiplier
    print(f'{args.number} * {args.multiplier} = {prod}')

if __name__=='__main__':
    argparser = argparse.ArgumentParser(description='My cool new script')
    argparser.add_argument('-m', '--multiplier', type=int, default=2, help='Multiplier (default: 2)')
    argparser.add_argument('number', type=int, help='Number to double')
    args = argparser.parse_args()
    main(args)