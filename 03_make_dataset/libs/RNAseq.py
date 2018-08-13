from glob import glob
from genome_vector import get_vector
from GTF import transcriptDict

def transcriptVector(genome, gtf, RNAseqFolder, splitGenome, typeOfFill, percentageOfOverPosition):
	#vector of genome fragments
	vector = get_vector(genome, splitGenome) #in the reallity this is a dict of chr: [vector of zeros]
	vectorAux = get_vector(genome, splitGenome) #an aux to know sum(fpkm)/how many sums where done in this position
	#transcript Dictionary
	transDict = transcriptDict(gtf) #transcript: [init,end,chr, gene]
	#looking for tsv files where fpkm is annoted
	tsvs = glob(RNAseqFolder+"/*.tsv")
	for tsv in tsvs:
		tsvFile = open(tsv,"r")
		aux = 0 # to avoid the first line
		aux2 = None
		for line in tsvFile:
			if aux !=0:
				split = line.split("\t")
				transcriptID = split[0]
				fpkm = float(split[6])
				if transcriptID in transDict:
					coords = transDict[transcriptID]
					#now we need to sum the fpkm to the current position and also we will add 1 to the positions in vectoraux
					#getting gene coords
					c1 = float(coords[0])
					c2 = float(coords[1])
					init = int(c1/(splitGenome*1000))
					end = int(c2/(splitGenome*1000))
					#percent init ocuppancy = (len(feature_init) * 100)/len(feature)
					#len(feature) = feature[2]-feature[1]
					#len(feature_init) = ((init_position+1)*(kb*1000)) - feature[1]
					percent_init_occupancy = ((((init+1)*(splitGenome*1000.))-c1)*100)/(c2-c1)
			
					#percent end ocuppancy = (len(feature_end) * 100)/len(feature)
					#len(feature) = feature[2]-feature[1]
					#len(feature_end) = feature[2] -((end_position)*(kb*1000)) 		
						
					percent_end_occupancy = ((c2-(end*(splitGenome*1000.)))*100)/(c2-c1)
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
							aux2 = vector[transDict[transcriptID][2]] # <------------------- Este splitted es el cromosoma actual
							if typeOfFill == "decimal":
								aux2[i] +=1
							if typeOfFill == "binary":
								aux2[i] = 1
							if typeOfFill == "average":
								#we will use an auxiliar vector to know how man times it was modified
								vectorAux[transDict[transcriptID][2]][i] += 1 
								aux2[i] += fpkm
								#print fpkm
							vector[transDict[transcriptID][2]] = aux2				
						i += 1	
			aux = 1
		tsvFile.close()

	#Now we exit from the tsv loop, so is time to divide if typeOfFill was average
	if typeOfFill == "average":
		for vect in vector.items():
			i = 0
			for fpkm in vect[1]:
				if fpkm != 0:
					vector[vect[0]][i] /= vectorAux[vect[0]][i]
				i += 1

	return vector
if __name__ == "__main__":
	print ("you can use it only as a lib. exiting")
	#transcriptVector("../../04_data/reference_genome/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna", "../../04_data/reference_genome/gencode.v24.primary_assembly.annotation-tRNAs-ERCC_phiX.gtf","../../04_data/K562/RNA-seq/total", 0.2, "average", 30)



