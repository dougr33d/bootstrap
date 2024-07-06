#!/bin/sh
"exec" "$(dirname $(readlink -f $0))/venv/bin/python3" "$0" "$@"

"""centrifuge is a script that splits a single log file into separate log files based on a config file."""

import argparse
import pprint as pp
import yaml
import typing
import re

#from libreed.helpers import banner,text_to_n_rows,do_cmd

def parse_config(cfg_file: typing.IO) -> dict:
    """Parse a YAML centrifuge config file and return the dict"""
    d = yaml.safe_load(cfg_file)

    # Compile regexes for performance
    for mat in d['matches']:
        mat['recmp'] = re.compile(mat['regex'])

    return d

def spin_it(cfg: dict, fn_log: str) -> dict:
    """Given the config dict and a log file, spin out to its contstituent parts"""
    # matches:
    # - match: '^@\[(\d+)\] .*unit:IC'
    #     group: 'IC'

    cfg_matches = cfg['matches']

    groups = {}
    with open(fn_log, 'r') as fh_log:
        for line in fh_log:
            first_match = next((mat for mat in cfg_matches if mat['recmp'].search(line)))
            group = first_match['group']
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

    cfg    = parse_config(args.config)
    groups = spin_it(cfg, args.logfile)

    for group,grpdict in groups.items():
        new_log = make_filename_from_group(args.logfile, group)
        with open(new_log, 'w') as fh_new:
            fh_new.writelines(grpdict['lines'])



if __name__=='__main__':
    argparser = argparse.ArgumentParser(description='Split a single log file into N separate log files')
    argparser.add_argument('config', type=argparse.FileType('rb'), help='YAML config file')
    # logfile is a str b/c we need to do string manip on filename
    argparser.add_argument('logfile', type=str, help='Log file to split')
    argparse_args = argparser.parse_args()
    main(argparse_args)
