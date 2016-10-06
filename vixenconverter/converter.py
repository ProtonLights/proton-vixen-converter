#!/usr/bin/env python3

from docopt import docopt

help_message = """Proton - Vixen Converter

Usage:
    converter.py <file>...
    converter.py --version
    converter.py (-h | --help)

Options:
    --version   Show version
    -h --help   Show this message
"""

def convert(file):
    print(file)

def run():
    arguments = docopt(help_message, version='Vixen Converter 0.0.1')
    files = arguments['<file>']
    for file in files:
        convert(file)

if __name__ == '__main__':
    run()
