#!/bin/sh
"exec" "$(dirname $(readlink -f $0))/venv/bin/python3" "$0" "$@"

"""centrifuge is a script that splits a single log file into separate log files based on a config file."""

import argparse
import pprint as pp
import yaml
import typing
from dataclasses import dataclass
import re
from functools import cache

@dataclass
class MatchGroup:
    group: str
    regex: str

    def __hash__(self):
        return hash((self.group, self.regex))

    @property
    @cache
    def recmp(self) -> typing.Any:
        return re.compile(self.regex)

def parse_config(cfg_file: typing.IO) -> list[MatchGroup]:
    """Parse a YAML centrifuge config file and return the dict"""
    d = yaml.safe_load(cfg_file)
    matgroups = []

    # Compile regexes for performance
    for mat in d['matches']:
        matgroups.append(MatchGroup(**mat))

    return matgroups

def find_first_match(args: typing.Any, matgroups: list[MatchGroup], line: str) -> MatchGroup:
    try:
        first_match = next((mg for mg in matgroups if mg.recmp.search(line)))
        return first_match
    except StopIteration as e:
        if args.strict:
            print(f"Could not find group matching {line}")
            raise(e)
        else:
            return MatchGroup(args.default_group, r'')

def spin_it(args: typing.Any, matgroups: list[MatchGroup], fn_log: str) -> dict:
    """Given the match groups and a log file, spin out to its contstituent parts"""
    # matches:
    # - match: '^@\[(\d+)\] .*unit:IC'
    #     group: 'IC'

    groups: dict[str, dict] = {}
    with open(fn_log, 'r') as fh_log:
        for line in fh_log:
            first_match = find_first_match(args, matgroups, line)
            group = first_match.group
            if group not in groups:
                groups[group] = { 'lines':[] }
            groups[group]['lines'].append(line)

    return groups

def make_filename_from_group(fn_log: str, groupname: str) -> str:
    """Create a new filename given a log filename and a group.
    
    Add '.groupname' before the first dot; if no dots are in the filename, add '.groupname' to the end of the filename.
    """

    if '.' in fn_log:
        return re.sub(r'\.', f".{groupname}.", fn_log, count=1)
    else:
        return f"{fn_log}.{groupname}"

def main(args):
    """Main function"""

    matgroups = parse_config(args.config)
    groups = spin_it(args, matgroups, args.logfile)

    for group,grpdict in groups.items():
        new_log = make_filename_from_group(args.logfile, group)
        with open(new_log, 'w') as fh_new:
            fh_new.writelines(grpdict['lines'])



if __name__=='__main__':
    argparser = argparse.ArgumentParser(description='Split a single log file into N separate log files')
    argparser.add_argument('config', type=argparse.FileType('rb'), help='YAML config file')
    # logfile is a str b/c we need to do string manip on filename
    argparser.add_argument('logfile', type=str, help='Log file to split')
    argparser.add_argument('-s', '--strict', default=False, action='store_true', help='Strict mode (default: no catch-all default group)')
    argparser.add_argument('-d', '--default-group', type=str, default='OTHER', help='Catch-all group name (ignored in strict mode)')
    argparse_args = argparser.parse_args()
    main(argparse_args)
