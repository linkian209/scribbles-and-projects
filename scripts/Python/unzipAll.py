# Name: unzipAll.py
# Description: Unzips all files in the Source Directory into the Drain Directory
# Author: Ian Drake Copyright 2015

import os
import sys
import zipfile
import fnmatch

def printUsage():
	print("Expected Usage: unzipAll.py -s <Source Directory> -d <Drain Directory>")

def main(argv=sys.argv):
	# Parse Inputs
	if(len(argv) - 1 != 4):
		printUsage()
		sys.exit(1)
	i = 1
	while(i < len(argv)):
		if(argv[i] == '-s'):
			if(len(argv) > i):
				i = i + 1
				sourceDir = argv[i]
		elif(argv[i] == '-d'):
			if(len(argv) > i):
				i = i + 1
				drainDir = argv[i]
		else:
			print("Unrecognized option "+argv[i])
			printUsage()
			sys.exit(1)
		i = i + 1
	
	print("Starting extraction from " + sourceDir + " to " + drainDir + ".....")
	print("-------------------------------------------------------------------")
	
	# Get all zip files and unzip them into the drain directory
	pattern = "*.zip"

	for root,dirs,files in os.walk(sourceDir):
		for filename in fnmatch.filter(files,pattern):
			print("Extracting "+os.path.join(root,filename))
			zipfile.ZipFile(os.path.join(root,filename)).extractall(os.path.join(drainDir,os.path.splitext(filename)[0]))

	print("-------------------------------------------------------------------")
	print("Extraction Complete!")
# Invoke the Main Routine
#--------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
#--------------------------------------------------------------------------------------