#!/usr/bin/env python
from mutagen import File
import sys, os

if len(sys.argv) < 2:
	print "Need a file."
	sys.exit(1)

fName = sys.argv[1]
oName = os.path.join(os.path.dirname(fName),"acoustics-art.tmp.jpg")
print "Extracting art from \033[1;34m%s\033[0m..." % fName,

fObj  = File(fName)

def writeData(data):
	print "\033[1;32mFound!\033[0m"
	f = open(oName,'w')
	f.write(data)
	f.close()
	sys.exit(0)

if "pictures" in dir(fObj):
	print "Checking pictures...",
	if len(fObj.pictures) > 0:
		writeData(fObj.pictures[0].data)
else:
	print "Checking tags...",
	if "APIC:" in fObj.tags:
		writeData(fObj.tags["APIC:"].data)

print "\033[1;31mNothing.\033[0m"
sys.exit(2)
