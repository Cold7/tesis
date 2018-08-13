"""
vectorData

Module that through intersectBed parse data from bed files and then, through genome_vector get a zero vector to fill data with features according its position

for more information please write to contrerasriquelme.sebastian@gmail.com
"""

import numpy
from intersectBed import intersect
from genome_vector import get_vector
from glob import glob


def tfFeaturedVector(path, percentage, genome, splitGenome, typeOfFill, percentageOfOverPosition): #tipeOfFill sera binario o decimal y percentageOfOverPosition is a percentagen needed to keep in a group
	#reading the list of TFs
	tfFile = open("./dat/TFs.csv","r")
	tfList = []
	for line in tfFile:
		if line[0] != "#": #if the current line is not a comment
			aux = line.split(",")
			if aux[3] == "Yes":
				tfList.append(aux[1])

	tfFile.close()
	tfFolders = glob(path+"*/")
	
	dictZeroVectors = get_vector(genome, splitGenome)
	
	for tfFolder in tfFolders:
		currentTF = tfFolder.split("/")[-2].replace("-human","")
		if currentTF in tfList:
			#getting the current features to use
			features = intersect(tfFolder,percentage)
			#getting dictionary of zeros for each portion of the genome
			for feature in features:
				init = int(feature[1]/(splitGenome*1000))
				end = int(feature[2]/(splitGenome*1000))
				#percent init ocuppancy = (len(feature_init) * 100)/len(feature)
				#len(feature) = feature[2]-feature[1]
				#len(feature_init) = ((init_position+1)*(kb*1000)) - feature[1]
				percent_init_occupancy = ((((init+1)*(splitGenome*1000.))-feature[1])*100)/(feature[2]-feature[1])

				#percent end ocuppancy = (len(feature_end) * 100)/len(feature)
				#len(feature) = feature[2]-feature[1]
				#len(feature_end) = feature[2] -((end_position)*(kb*1000)) 		
			
				percent_end_occupancy = ((feature[2]-(end*(splitGenome*1000.)))*100)/(feature[2]-feature[1])
		
				i = init
				while i <= end:
					to_mark = True # to know if I need to mark that position
					if i == init:
						if percent_init_occupancy < percentageOfOverPosition:
							to_mark == False
					if i == end:
						if percent_end_occupancy < percentageOfOverPosition:
							to_mark == False
			
					if to_mark == True:
						aux = dictZeroVectors[feature[0]]
						if typeOfFill == "decimal":
							aux[i] +=1
						if typeOfFill == "binary":
							aux[1] = 1
						dictZeroVectors[feature[0]] = aux
				
					i+=1
	
	return dictZeroVectors

			
if __name__ == "__main__":
	print ("Please type help(\"vectorData\")")
	#getFeaturedVector("../../04_data/K562/DNA_methylation",100,"../../04_data/reference_genome/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna", 0.1,"decimal", 30)
