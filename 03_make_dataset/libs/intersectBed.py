"""
Module that return coords for a single bed file or a consensus (all or only those conserved through bed files).

This module require to have installed bedTools. For more information about how to install it, please read http://bedtools.readthedocs.io/en/latest/content/installation.html

for more information please write to contrerasriquelme.sebastian@gmail.com
"""
from glob import glob
from subprocess import Popen, PIPE


def singleBed(bedFile):
	"""
	Function to parse bed file and return a list of list with chr, coord1, coord2
	"""
	toReturn = []
	bed = open(bedFile,"r")
	for line in bed:
		toReturn.append([line.split("\t")[0],int(line.split("\t")[1]),int(line.split("\t")[2])])
	bed.close()
	return toReturn

def multiBed(bedList, percentage):
	"""
	Function that take a list of bed files and percentage to merge features in the chromatin through multiIntersectBed
	"""
	toReturn = []
	cmd = "multiIntersectBed -i "
	for l in bedList:
		cmd += l+" "
	cmd = cmd.split(" ")[:-1]
	process = Popen(cmd, stdout=PIPE)
	for line in process.stdout:
		lineSplitted = (line.decode()).split("\t")
		if (float(lineSplitted[3])/len(bedList)*100) >= percentage:
			toReturn.append([lineSplitted[0],int(lineSplitted[1]),int(lineSplitted[2])])
	return toReturn
		
	

def intersect(path_with_features, percentage):
	"""
	main module. This module take a path for bed files and a percentage to keep features present in the chromosomes (default: 100). Then call a function depending the number of files to generate a consensus and return a list of chr, coord1 and coord2
	"""
	if percentage <= 0 or percentage > 100:
		print ("percentage can not be less or equal than 0 or higher than 100. exiting")
		exit()

	bedFiles = glob(path_with_features+"/*.bed")
	if len(bedFiles) == 0:
		return []
	elif len(bedFiles) == 1:
		return singleBed(bedFiles[0])
	else:
		return multiBed(bedFiles, percentage)

if __name__ == "__main__":
	print ("Please type help(\"intersectBed\")")



