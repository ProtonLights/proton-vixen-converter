from VixenLib.VixenFile import VixenFile
import sys
import os

pargs={'filename':None,'metadata':False}

for arg in sys.argv:
    if arg.startswith('file='):
        pargs['filename'] = arg[5:]
    if arg == '-m':
        pargs['metadata']=True

if pargs['filename']==None:
    raise FileNotFoundError("Filename not specified")

file = os.path.splitext(pargs['filename'])
if file[-1] == ".vix":
    vf = VixenFile.VixenSequence(pargs['filename'])
elif file[-1] == ".pro":
    vf = VixenFile.VixenProfile(pargs['filename'])
else:
    sys.stderr.write("Could not recognize the file extension {0}".format(file[-1]))

def run():
    if pargs['metadata']:
        print(vf.getMetadata())
    else:
        print(vf.dump())

if not sys.flags.interactive:
    run()
else:
    print("Entering interactive mode.")
    #print("Entering interactive mode.  Please call allstop() before exit() to avoid a hang condition.")
    run()