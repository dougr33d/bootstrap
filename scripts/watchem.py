#!/bin/sh
"exec" "$(dirname $(readlink -f $0))/venv/bin/python3" "$0" "$@"

import argparse
#import pprint as pp
import shutil
import logging

from libreed.helpers import banner,text_to_n_rows,do_cmd

"""Watchem is a helper script to help you watch multiple files."""

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

def render(thing: str, nrows: int, ncols: int) -> str:
    """Render a thing (command or file) for n rows"""
    lines = []

    rtn = None
    if thing[0] == '@':
        rtn = do_cmd(thing[1:], check=False)
    else:
        rtn = do_cmd(f'tail -n {nrows} {thing}', check=False)

    lines.append(banner(thing,ncols))
    lines.append(text_to_n_rows(rtn, nrows-1))

    return "\n".join(lines)

def main():
    """Main function"""

    argparser = argparse.ArgumentParser(description='Watch commands or files')
    argparser.add_argument('things', type=str, nargs='+', help='Commands or files to watch (prepend commands with @)')
    args = argparser.parse_args()

    term_size = shutil.get_terminal_size()
    tot_rows  = term_size.lines - 1
    tot_cols  = term_size.columns

    rows_per_thing = tot_rows // len(args.things)
    for nth,thing in enumerate(args.things):
        nrows = rows_per_thing
        if nth == len(args.things)-1:
            # get the excess
            nrows = rows_per_thing + (tot_rows % rows_per_thing)
        print(render(thing, nrows, tot_cols))

if __name__=='__main__':
    main()
