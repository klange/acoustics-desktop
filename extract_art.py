#!/usr/bin/env python
from mutagen import File
import sys, os

oNameJPG = "acoustics-art.jpg"
oNamePNG = "acoustics-art.png"

def writeData(obj):
	print "\033[1;32mFound!\033[0m"
	if obj.mime.find("jpeg") > -1:
		oName = oNameJPG
	elif obj.mime.find("png") > -1:
		oName = oNamePNG
	else:
		print "Unknown filetype: ", t.mime
		return 1
	f = open(oName,'w')
	f.write(obj.data)
	f.close()
	return 0

def extractArt(fName):
	global oNameJPG, oNamePNG
	oNameJPG = os.path.join(os.path.dirname(fName),"acoustics-art.jpg")
	oNamePNG = os.path.join(os.path.dirname(fName),"acoustics-art.png")
	if os.path.exists(oNameJPG) or os.path.exists(oNamePNG):
		print "Skipping \033[1;34m%s\033[0m, already have art." % fName
		return 2
	print "Extracting art from \033[1;34m%s\033[0m..." % fName,

	fObj  = File(fName)

	if "pictures" in dir(fObj):
		print "Checking pictures...",
		if len(fObj.pictures) > 0:
			return writeData(fObj.pictures[0])
	else:
		print "Checking tags...",
		if "APIC:" in fObj.tags:
			return writeData(fObj.tags["APIC:"])
	print "\033[1;31mNothing.\033[0m"
	return 1

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Need a file."
		sys.exit(1)
	extractArt(sys.argv[1])
	sys.exit(2)
