"""Helper functions"""
import subprocess

def do_cmd(command: str, check: bool = False) -> str:
    """Given a command, run the command and return the output"""
    rtn = subprocess.run(command.split(' '), stdout=subprocess.PIPE, check=check).stdout.decode('utf-8')
    return rtn

def banner(text: str, width: int) -> str:
    """Given a string, return a width-wide banner that wraps the string in hashes."""
    banner_char = '#'
    llen = (width - len(text) - 2) // 2
    rlen = width - len(text) - 2 - llen
    lpad = banner_char * llen
    rpad = banner_char * rlen
    line = f"{lpad} {text} {rpad}"
    return line

def text_to_n_rows(text: str, num_rows: int) -> str:
    """Given a multiline string, truncate or pad it to num_rows rows."""
    lines = text.split('\n')
    if len(lines) > num_rows-1:
        lines = lines[-1*(num_rows-1):]
    if len(lines) < num_rows:
        lines.extend(['~'] * (num_rows - len(lines)))
    assert len(lines) == num_rows
    return '\n'.join(lines)
