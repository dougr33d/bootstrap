#!/bin/env python3.12

import argparse
"""centrifuge is a script that splits a single log file into separate log files based on a config file."""

#import pprint as pp
import typing
from dataclasses import dataclass
import re
from functools import lru_cache
import logging
import sys

import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

@dataclass
class MatchGroup:
    """MatchGroup is a class that encapsulates match info from the centrifuge config."""
    group: str
    regex: str

    def __hash__(self):
        """Make the class hashable"""
        return hash((self.group, self.regex))

    @property
    @lru_cache(maxsize=128)
    def recmp(self) -> typing.Any:
        """Cached property to return compiled regex"""
        return re.compile(self.regex)

def parse_config(cfg_file: typing.IO, strict: bool = False, dflt_group: str = 'MISC') -> list[MatchGroup]:
    """Parse a YAML centrifuge config file and return the dict"""

    logger.debug(f"Parsing config stream {cfg_file}")

    d = yaml.safe_load(cfg_file)
    matgroups = []

    # Compile regexes for performance
    for mat in d['matches']:
        matgroups.append(MatchGroup(**mat))

    if not strict:
        matgroups.append(MatchGroup(dflt_group, r''))

    return matgroups

def find_first_match(matgroups: list[MatchGroup], line: str) -> MatchGroup:
    """Find and return the first matching matchgroup."""
    try:
        first_match = next((mg for mg in matgroups if mg.recmp.search(line)))
        return first_match
    except StopIteration:
        logger.error(f"Could not find group matching '{line.strip()}'...")
        logger.error("consider running without --strict, or add a catch-all group")
        sys.exit(-1)

def spin_it(matgroups: list[MatchGroup], fn_log: str) -> dict:
    """Given the match groups and a log file, spin out to its contstituent parts"""

    groups: dict[str, dict] = {}
    with open(fn_log, 'r', encoding='utf-8') as fh_log:
        logger.debug(f"Reading {fn_log}")
        for line in fh_log:
            first_match = find_first_match(matgroups, line)
            group = first_match.group
            if group not in groups:
                groups[group] = { 'lines':[] }
            groups[group]['lines'].append(line)

    return groups

def make_filename_from_group(fn_log: str, groupname: str) -> str:
    """Create a new filename given a log filename and a group.
    
    Add '.groupname' before the first dot; if no dots are in the filename, add '.groupname' to the end of the filename.
    """

    assert "/" not in fn_log
    if '.' in fn_log:
        return re.sub(r'\.', f".{groupname}.", fn_log, count=1)
    return f"{fn_log}.{groupname}"

def main():
    """Main function"""

    argparser = argparse.ArgumentParser(description='Split a single log file into N separate log files')
    argparser.add_argument('config', type=argparse.FileType('rb'), help='YAML config file')
    argparser.add_argument('logfile', type=str, help='Log file to split') # logfile is a str b/c we need to do string manip on filename
    argparser.add_argument('-s', '--strict', default=False, action='store_true', help='Strict mode (default: no catch-all default group)')
    argparser.add_argument('-d', '--default-group', type=str, default='OTHER', help='Catch-all group name (ignored in strict mode)')
    argparser.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose output')
    args = argparser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    matgroups = parse_config(args.config, args.strict, args.default_group)
    groups = spin_it(matgroups, args.logfile)

    for group,grpdict in groups.items():
        fn_log = args.logfile.split("/")[-1]
        new_log = make_filename_from_group(fn_log, group)
        with open(new_log, 'w', encoding='utf-8') as fh_new:
            fh_new.writelines(grpdict['lines'])
            nlines = len(grpdict['lines'])
            logger.info(f"Wrote {nlines:4d} line(s) to {new_log}")

if __name__=='__main__':
    main()
