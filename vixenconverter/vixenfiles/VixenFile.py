"""VixenFile
Library designed to read Vixen Lights sequences and profiles.
Written by Ryan Smith <smit7595@umn.edu>, modified by Ryan Fredlund <fredl027@umn.edu>.
This library is available under the MIT license found in the LICENSE file.

VixenFile takes a Vixen sequence or profile and creates an XML tree for it, warning the user 
if it detects the file is not a sequence or profile.
"""

import xml.etree.ElementTree as ET
import sys


class VixenFile(object):
    def __init__(self, file_path):
        # Set convert=false at runtime to prevent automatic file detection.
        #  Otherwise, this class will convert to the approprate class based on the type of Vixen file detected
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        if self.root.tag == 'Program':
            sys.stdout.write('VIXEN_STATUS: Detected Vixen sequence\n')
        elif self.root.tag == 'Profile':
            sys.stdout.write('VIXEN_STATUS: Detected Vixen profile.\n')
        else:
            sys.stderr.write('VIXEN_ERROR: Loaded file was not recognized (could not find a valid root tag).  Root tag found: {0}\n'.format(self.root.tag))

    def dump(self):
        raise NotImplemented("You can't call this right now without defining the type of Vixen file")

    def get_type(self):
        return self.root.tag
