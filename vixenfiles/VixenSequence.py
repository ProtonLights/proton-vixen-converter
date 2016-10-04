
import sys
import os
import base64
import numpy
from VixenFiles.VixenFile import VixenFile
from VixenFiles.VixenProfile import VixenProfile
from Patching.Patcher import Patcher

class VixenSequence(VixenFile, object):
    def __init__(self, filename, vixPath, patcher):
        super().__init__(filename)

        self.patcher = patcher
        self.vixPath = vixPath

        if self.getType() != 'Program':
            raise VixenException("File is not a Vixen sequence")
        self.metadata={}
        self.metadata['engine'] = self.root.find('EngineType').text

        if self.metadata['engine'] != "Standard":
            sys.stderr.write('VIXEN_WARN: Loaded Vixen sequence is not of type Standard. It may not be readable by this program. (type is {0})'.format(self.data['EngineType']))

        sys.stderr.write('VIXEN_WARN: At this time, we can only extract sequence metadata and event values.  Plugins are not yet supported.\n')
        
        audioel = self.root.find('Audio')

        self.metadata['title'] = audioel.text
        self.audio = {'title':audioel.text, 'filename':audioel.attrib['filename'], 'duration':int(audioel.attrib['duration'])}

        self.metadata['time'] = int(self.root.find('Time').text)
        self.metadata['eventperiod'] = int(self.root.find('EventPeriodInMilliseconds').text)
        self.metadata['minlevel'] = int(self.root.find('MinimumLevel').text)
        self.metadata['maxlevel'] = int(self.root.find('MaximumLevel').text)
        self.metadata['profile'] = self.root.find('Profile').text
        self.events = self.extract_events(self.root.find('EventValues').text)

    def extract_events(self, eventvalues):
        estring = base64.b64decode(eventvalues)
        numev = int(numpy.ceil(self.metadata['time']/self.metadata['eventperiod']))
        numch = int(len(estring)/numev)
        events = numpy.zeros((numch + 1, numev), dtype=numpy.uint8)

        for ch in range(numch):
            for ev in range(numev):
                events[ch][ev] = estring[ev+numev*ch];

        # Fix vixen file order
        vixenProfile = VixenProfile.make_vixen_profile( \
                self.metadata['profile'] + '.pro', self.vixPath)
        def makeIndex(l):
            k = enumerate(l)
            index = list(map(lambda x: x[0], sorted(k, key=lambda x: x[1])))
            return numpy.array(index)
        reorderedEvents = events[makeIndex(vixenProfile.getOutputOrder())]

        # Patch the channels
        patchIndex = self.patcher.makePatchIndex()
        reorderedEvents = numpy.vstack([reorderedEvents, ([0] * numev)])
        patchedEvents = reorderedEvents[numpy.array(patchIndex)]

        # Zero out unused channels
        zeroChannel = numpy.zeros((1, numev), dtype=numpy.uint8)
        for ind, val in enumerate(patchIndex):
            if val == -1:
                patchedEvents[ind] = zeroChannel

        finalEvents = numpy.transpose(patchedEvents)
        self.metadata['numch'] = numch
        self.metadata['numev'] = numev
        return finalEvents

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
    def make_vixen_sequence(file, vix_path, patcher):
        if os.path.splitext(file)[-1] != ".vix":
            raise ValueError("Not a .vix file")

        if vix_path is None:
            raise VixenException("No path specified")

        return VixenSequence(vix_path + "/Sequences/" + file, vix_path, patcher)

