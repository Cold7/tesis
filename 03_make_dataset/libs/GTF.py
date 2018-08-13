"""
gtfVector

Starting from a genome and a GTF file, it return a vector of gene

for more information please write to contrerasriquelme.sebastian@gmail.com
"""

from genome_vector import get_vector

def geneVector(genome, splitGenome, GTF, typeOfFill, percentageOfOverPosition):

	#getting gene vector for each chr (its a dict)
	vector = get_vector(genome, splitGenome)
	gtfGene = []
	gtf = open(GTF,"r")
	for line in gtf:
		splittedLine = line.split("\t")
		geneID = splittedLine[8].split("\"")[1]
		if "spikein	exon" not in line:
			if (splittedLine[2] == "gene" or "ENSG" not in geneID):
				#getting gene coords
				c1 = float(splittedLine[3])
				c2 = float(splittedLine[4])
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
						aux = vector[splittedLine[0]]
						if typeOfFill == "decimal":
							aux[i] +=1
						if typeOfFill == "binary":
							aux[i] = 1
						vector[splittedLine[0]] = aux
						
					i+=1

	return vector


def transcriptDict(GTF):	
	dictToReturn = {}
	gtf = open(GTF,"r")	
	t = []
	for line in gtf:
		splitted = line.split("\t")
		geneID = splitted[8].split("\"")[1]
		transcriptID = splitted[8].split("; ")[1].split("\"")[1]
		if ((splitted[2] == "transcript") or (transcriptID == geneID) ) and "spikein	exon" not in line:
			spl2=line.split("transcript_id")[1].split(";")[0]
			dictToReturn[transcriptID]=[splitted[3],splitted[4],splitted[0], geneID]

			
	return dictToReturn
	
if __name__ == "__main__":
	print ("Please type help(\"vectorData\")")
	#transcriptDict("/home/sebas/Desktop/predictor/04_data/reference_genome/gencode.v24.primary_assembly.annotation-tRNAs-ERCC_phiX.gtf")


