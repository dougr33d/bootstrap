#!/bin/sh
"exec" "$(dirname $(readlink -f $0))/venv/bin/python3" "$0" "$@"

import argparse
#import pprint as pp
import shutil
import subprocess

from libreed.helpers import banner,text_to_n_rows

def render(cmd: str, nrows: int, ncols: int) -> str:
    """Render a command/file for n rows"""
    lines = []

    rtn = subprocess.run(f'tail -n {nrows} {cmd}'.split(' '), stdout=subprocess.PIPE, check=False).stdout.decode('utf-8')

    lines.append(banner(cmd,ncols))
    lines.append(text_to_n_rows(rtn, nrows-1))

    return "\n".join(lines)

def main(args):
    """Main function"""
    commands = args.commands

    term_size = shutil.get_terminal_size()
    tot_rows  = term_size.lines - 1
    tot_cols  = term_size.columns

    rows_per_cmd = tot_rows // len(commands)
    for nth,cmd in enumerate(commands):
        nrows = rows_per_cmd
        if nth == len(commands)-1:
            # get the excess
            nrows = rows_per_cmd + (tot_rows % rows_per_cmd)
        print(render(cmd, nrows, tot_cols))

if __name__=='__main__':
    argparser = argparse.ArgumentParser(description='Watch commands or files')
    argparser.add_argument('commands', type=str, nargs='+', help='Commands or files to watch')
    argparse_args = argparser.parse_args()
    main(argparse_args)
