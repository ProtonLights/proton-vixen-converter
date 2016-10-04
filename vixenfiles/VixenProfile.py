import sys
import os
from VixenFiles.VixenFile import VixenFile

class VixenProfile(VixenFile, object):
    def __init__(self,filename):
        super().__init__(filename)
        if self.getType() != 'Profile':
            raise VixenException("File is not a Vixen profile")

    def getOutputOrder(self):
        order = self.root.find("Outputs").text
        return list(map(lambda x: int(x), order.split(',')))


    # Factory method to create a VixenProfile
    # Checks if file path/extension is valid
    # and builds sequence path from vix_path and file
    @staticmethod
    def make_vixen_profile(file, vix_path):
        if os.path.splitext(file)[-1] != ".pro":
            raise ValueError("Not a .pro file")

        if vix_path is None:
            raise VixenException("No path specified")

        return VixenProfile(vix_path + "/Profiles/" + file)
