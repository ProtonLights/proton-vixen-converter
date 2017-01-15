import base64
import os
import sys

import numpy

from vixenfiles import VixenFile, VixenException


class VixenSequence(VixenFile):
    def __init__(self, seq_path):
        super().__init__(seq_path)

        if self.get_type() != 'Program':
            raise VixenException("File is not a Vixen sequence")
        self.metadata={}
        self.metadata['engine'] = self.root.find('EngineType').text

        if self.metadata['engine'] != "Standard":
            sys.stderr.write('VIXEN_WARN: Loaded Vixen sequence is not of type Standard. It may not be readable by this program. (type is {0})'.format(self.data['EngineType']))

        sys.stderr.write('VIXEN_WARN: At this time, we can only extract sequence metadata and event values.  Plugins are not yet supported.\n')
        
        audio_element = self.root.find('Audio')

        self.metadata['title'] = "".join(seq_path.split('/')[::-1]).split('.')[0]
        self.audio = {
            'title': audio_element.text,
            'filename': audio_element.attrib['filename'],
            'duration': int(audio_element.attrib['duration'])
        }

        self.metadata['time'] = int(self.root.find('Time').text)
        self.metadata['eventperiod'] = int(self.root.find('EventPeriodInMilliseconds').text)
        self.metadata['minlevel'] = int(self.root.find('MinimumLevel').text)
        self.metadata['maxlevel'] = int(self.root.find('MaximumLevel').text)
        self.metadata['profile'] = self.root.find('Profile').text
        self.events = self.extract_events(self.root.find('EventValues').text)

    def extract_events(self, event_values):
        estring = base64.b64decode(event_values)
        numev = int(numpy.ceil(self.metadata['time'] / self.metadata['eventperiod']))
        numch = int(len(estring) / numev)
        events = numpy.zeros((numch, numev), dtype=numpy.uint8)

        for ch in range(numch):
            for ev in range(numev):
                events[ch][ev] = estring[ev + numev * ch];

        self.metadata['numch'] = numch
        self.metadata['numev'] = numev

        return events

    def dump(self):
        return {"metadata":self.metadata,"audio":self.audio,"events":self.events}

    def get_metadata(self):
        return self.metadata

    def get_audio(self):
        return self.audio

    def get_profile(self):
        return self.metadata['profile']

    def get_events(self):
        return self.events

    @staticmethod
    # Factory method to create a VixenSequence
    # Checks if file path/extension is valid
    # and builds sequence path from vix_path and file
    def make_vixen_sequence(seq_path):
        if seq_path is None:
            raise VixenException("No path specified")

        if os.path.splitext(seq_path)[-1] != ".vix":
            raise ValueError("Not a .vix file")

        return VixenSequence(seq_path)

