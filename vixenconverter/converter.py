#!/usr/bin/env python3

from docopt import docopt
import json
import os
from vixenfiles import VixenSequence,VixenProfile

help_message = """Proton - Vixen Converter

Usage:
    converter.py import-sequence <admin-key> <seq-file> <audio-file> <layout-id>
    converter.py import-layout <pro-file> <default-dmx>
    converter.py --version
    converter.py (-h | --help)

Options:
    --version   Show version
    -h --help   Show this message
"""



def add_seq_to_proton_cli(seq, seq_file, key_file, audio_file, layout_id):
    """Executes the proton_cli command 'new-vixen-sequence' with all appropriate parameters."""

    # new-vixen-sequence <admin-key> <name> <music-file> <frame-duration> <data-file> <layout-id>
    seq_md = seq.get_metadata()

    print("Running proton_cli...", flush=True)

    os.execlp('proton_cli',
        'proton_cli',
        'new-vixen-sequence',
        key_file,
        seq_md['title'],
        audio_file,
        str(seq_md['time']),
        str(seq_md['eventperiod']),
        seq_file,
        layout_id)


def add_layout_to_proton_cli(layout_file):
    """Executes the proton_cli command 'new-layout' with all appropriate parameters."""

    # new-layout <layout-file>
    print("Running proton_cli...", flush=True)
    os.execlp('proton_cli', 'proton_cli', 'new-layout', layout_file)


def import_profile(pro_file, default_channel):
    """Converts a Vixen profile (.pro) to a Proton layout and adds it to proton_cli."""

    # Get profile
    pro = VixenProfile.make_vixen_profile(pro_file)
    channels = pro.get_channels(default_channel)

    # Write layout data as JSON to file
    layout = {
        'layoutName': pro.name.replace('_', ''),
        'channels': channels
    }
    layout_json = json.dumps(layout)
    layout_file_name = pro.name + "_layout.json"
    ofile = open(layout_file_name, mode='w')
    ofile.write(layout_json)
    ofile.flush()
    ofile.close()

    # Add to proton-cli
    add_layout_to_proton_cli(layout_file_name)


def import_sequence(seq_file, key_file, audio_file, layout_id):
    """Converts a Vixen sequence (.vix) to a Proton sequence and imports it into proton_cli."""

    # Get sequence
    seq = VixenSequence.make_vixen_sequence(seq_file)
    seq_metadata = seq.get_metadata()
    
    # Write sequence data as JSON to file
    seq_json = json.dumps(seq.events.tolist())
    ofile_name = seq_metadata['title'] + ".json"
    ofile = open(ofile_name, mode='w')
    ofile.write(seq_json)
    ofile.flush()
    ofile.close()
    
    # Add to proton-cli
    add_seq_to_proton_cli(seq, ofile_name, key_file, audio_file, layout_id)


def run():
    """Runs correct command.

    Determines which command was run and delegates to the appropriate function 
    with all necessary parameters."""
    
    arguments = docopt(help_message, version='Vixen Converter 0.0.1')
    if arguments['import-sequence']:
        seq_file = arguments['<seq-file>']
        key_file = arguments['<admin-key>']
        audio_file = arguments['<audio-file>']
        layout_id = arguments['<layout-id>']
        import_sequence(seq_file, key_file, audio_file, layout_id)
    else:
        pro_file = arguments['<pro-file>']
        default_channel = int(arguments['<default-dmx>'])
        import_profile(pro_file, default_channel)


# Don't run if imported
if __name__ == '__main__':
    run()
