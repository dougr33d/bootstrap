#!/usr/bin/env python3.12

"""swapres is a script that cycles through screen rezzes."""

import argparse
# import pprint as pp
# import typing
# from dataclasses import dataclass
import re
# from functools import lru_cache
import logging
# import sys

# import yaml
from libreed.helpers import do_cmd

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

WHITELIST = ['2880x2400', '3840x2160', '2560x1600', '3840x1600']


def xrandr_line_to_rez(line: str) -> str:
    """Convert an xradr line to a resolution"""
    spl = line.split()
    return f"{spl[1]}x{spl[3]}"


def get_current_rez() -> str:
    """Return the current resolution"""

    command = "/usr/bin/xrandr --query"
    rtn = do_cmd(command, as_list=True)
    matline = [line for line in rtn if re.match(r'^\*', line)][0]
    rez = xrandr_line_to_rez(matline)
    return rez


def get_all_rezzes() -> list[str]:
    """Return a list of all resolutions supported in xrandr"""
    command = "/usr/bin/xrandr --query"
    rtn = do_cmd(command, as_list=True)
    lines = (line for line in rtn if re.search(r'\d+ x \d+', line))
    rezzes = [xrandr_line_to_rez(line) for line in lines]
    return rezzes


def change_to_rez(to_rez: str) -> None:
    """Change to the specified resolution"""
    command = f"xrandr -s {to_rez}"
    print(command)
    do_cmd(command)


def swap_res() -> None:
    all_rez = get_all_rezzes()
    val_rez = [r for r in all_rez if r in WHITELIST]
    this_rez = get_current_rez()

    start_from = len(val_rez) - 1
    if this_rez in val_rez:
        start_from = val_rez.index(this_rez)

    next_rez = val_rez[(start_from + 1) % len(val_rez)]

    change_to_rez(next_rez)


def main():
    """Main function"""

    argparser = argparse.ArgumentParser(description='Cycle through screen resolutione.')
    argparser.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose output')
    args = argparser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    swap_res()


if __name__ == '__main__':
    main()
