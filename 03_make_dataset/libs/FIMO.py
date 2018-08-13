import numpy
from intersectBed import intersect
from genome_vector import get_vector
from glob import glob

def FIMOVector(fimopath, genome, splitGenome, typeOfFill, percentageOfOverPosition, fimo_filter):
	fimoDict = {} #TFBM = NSITES
	fimoMotifs = open ("./dat/HOCOMOCOv11_full_HUMAN_mono_meme_format.meme","r")
	currentMotif = ""
	for line in fimoMotifs:
		if "MOTIF" in line:
			currentMotif = line[:-1].replace("MOTIF ","")
		if "nsites=" in line:
			fimoDict[currentMotif] = int(line[:-1].split("nsites= ")[-1])
	fimoMotifs.close

	folders = glob(fimopath+"/*/")
	dictZeroVectors = get_vector(genome, splitGenome)
	for folder in folders:
		file = open(folder+"fimo.txt","r")
		for line in file:
			if line[0] != "#":
				splt = line[:-1].split("\t")
				if fimoDict[splt[0]] >= fimo_filter:
					chr = splt[2]
					#print splt[1],splt[3], splt[4]
					init = int(int(splt[3])/(splitGenome*1000))
					end = int(int(splt[4])/(splitGenome*1000))
					#percent init ocuppancy = (len(feature_init) * 100)/len(feature)
					#len(feature) = feature[2]-feature[1]
					#len(feature_init) = ((init_position+1)*(kb*1000)) - feature[1]
					percent_init_occupancy = ((((init+1)*(splitGenome*1000.))-int(splt[3]))*100)/(int(splt[4])-int(splt[3]))
			
					#percent end ocuppancy = (len(feature_end) * 100)/len(feature)
					#len(feature) = feature[2]-feature[1]
					#len(feature_end) = feature[2] -((end_position)*(kb*1000)) 						
					percent_end_occupancy = ((int(splt[4])-(end*(splitGenome*1000.)))*100)/(int(splt[4])-int(splt[3]))
					
					#if init!=end:
					#	print init, end, percent_init_occupancy, percent_end_occupancy					
			
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
							
							aux = dictZeroVectors[chr]
							if typeOfFill == "decimal":
								aux[i] +=1
							if typeOfFill == "binary":
								aux[1] = 1
							dictZeroVectors[chr] = aux
							
						i+=1					
				
		file.close()

	return dictZeroVectors

			
if __name__ == "__main__":
	print ("Please type help(\"vectorData\")")
