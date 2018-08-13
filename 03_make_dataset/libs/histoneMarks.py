"""
vectorData

Module that through intersectBed parse data from bed files and then, through genome_vector get a zero vector to fill data with features according its position

for more information please write to contrerasriquelme.sebastian@gmail.com
"""

import numpy
from intersectBed import intersect
from genome_vector import get_vector
from glob import glob


def histoneFeaturedVector(path, percentage, genome, splitGenome, typeOfFill, percentageOfOverPosition, histoneMarks_by_type): #tipeOfFill sera binario o decimal y percentageOfOverPosition is a percentagen needed to keep in a group
	hmFolders = glob(path+"*/")
	hmDict = {}
	if histoneMarks_by_type == "together":
		hmDict["histone_marks"] = get_vector(genome, splitGenome)
	if histoneMarks_by_type == "unique":
		for hmFolder in hmFolders:
			hmDict[hmFolder.split("/")[-2].replace("-human","")] = get_vector(genome, splitGenome)
	
	for hmFolder in hmFolders:
		currentHM = hmFolder.split("/")[-2].replace("-human","")
		if histoneMarks_by_type == "together":
			currentHM = "histone_marks"		

		#getting the current features to use
		features = intersect(hmFolder,percentage)
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
					aux = hmDict[currentHM][feature[0]]
					if typeOfFill == "decimal":
						aux[i] +=1
					if typeOfFill == "binary":
						aux[i] = 1
					hmDict[currentHM][feature[0]] = aux
			
				i+=1
		
	return hmDict
			
if __name__ == "__main__":
	print ("Please type help(\"vectorData\")")
	#getFeaturedVector("../../04_data/K562/DNA_methylation",100,"../../04_data/reference_genome/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna", 0.1,"decimal", 30)
