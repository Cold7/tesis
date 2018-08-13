#importing libraries

import sys,os
import argparse   # arguments parser
import multiprocessing as mp
from glob import glob
from platform import platform


#the follow variable is defined here to know how to separate folders
#depending on the current OS (win or linux

separator = None

if "Windows" in platform():
	separator= "\\"
	#to know where are my libs
	sys.path.append(str(os.path.realpath(__file__))[:-8]+"\libs")

else:
	separator ="/"
	#to know where are my libs
	sys.path.append(str(os.path.realpath(__file__))[:-8]+"/libs")

# importing my own libraries
from vectorData import getFeaturedVector
from GTF import geneVector
from RNAseq import transcriptVector
from TF import tfFeaturedVector
from histoneMarks import histoneFeaturedVector
from FIMO import FIMOVector
from save import saveDataset

if __name__=="__main__":
		
	#input
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--genome", help="Path to genome file (in fasta format)", required = True)
	parser.add_argument("-cl", "--cell_line", help="Cell line name (default: None)", default="None")
	parser.add_argument("-s","--DNA_split", help="number of kb to split the DNA sequence. Default: 0.2", type = float, default=0.2)
	parser.add_argument("-p","--percentage", help="For some experiments you may need to merge them, so to do it you need to incluye a percentage of files that contain the feature. Default: 100", type = float, default = 100)
	parser.add_argument("-oc","--occupancy", help="If a feature fits in two position (or more) of the vector, you will need to set percentage of occupancy of the feature in the current position. Default: 30", type = float, default = 30)

	####################################
	##
	## GTF and gene arguments
	##
	####################################
	parser.add_argument("-gtf", "--GTF", help="Path to GTF file", required = True)
	parser.add_argument("-gfm","--gtf_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")
	
	####################################
	##
	## CTCF arguments
	##
	####################################
	parser.add_argument("-ctcf","--ctcfFolder", help="Folder where CTCF ChIP-seq results (in bed file) are located.", required = True)
	parser.add_argument("-cfm","--ctcf_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")
	
	####################################
	##
	## YY1 arguments
	##
	####################################
	parser.add_argument("-yy1","--yy1Folder", help="Folder where YY1 ChIP-seq results (in bed file) are located.", required = True)
	parser.add_argument("-yfm","--yy1_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")

	####################################
	##
	## DNase-seq arguments
	##
	####################################
	parser.add_argument("-dnaseq","--DHS_dnaseq_Folder", help="Folder where dnaseq results for DHS (in bed file) are located.", required = True)
	parser.add_argument("-dhsfm","--DHS_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")
	
	####################################
	##
	## DNA methylation arguments
	##
	####################################
	parser.add_argument("-dname","--methylation_Folder", help="Folder where dnaseq results for DHS (in bed file) are located.", required = True)
	parser.add_argument("-dmfm","--DNA_meth_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")
	
	####################################
	##
	## RNA-seq arguments
	##
	####################################
	parser.add_argument("-r","--RNA_Folder", help="Folder where RNAseq results (in bed file) are located.", required = True)
	parser.add_argument("-rfm","--RNA_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\", \"decimal\" or \"average\". Default: average", default="average")
	
	####################################
	##
	## TFs arguments
	##
	####################################
	parser.add_argument("-tf","--tfFolder", help="Folder where tf subfolders with ChIP-seq results (in bed file) are located.", required = True)
	parser.add_argument("-tfm","--tf_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")

	####################################
	##
	## Histone marks arguments
	##
	####################################
	parser.add_argument("-hm","--histoneMarksFolder", help="Folder where histone marks ChIP-seq results (in bed file) are located.", required = True)
	parser.add_argument("-hfm","--histoneMarks_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")
	parser.add_argument("-hbt","--histoneMarks_by_type", help="If you wish to get all histone marks in one vector or different vector of informations for histone mark. Options are \"together\"  or \"unique\". Default: decimal", default="together")
	
	####################################
	##
	## Fimo arguments
	##
	###################################	
	
	parser.add_argument("-ff", "--fimo_folder", help="Path to fimo folder. this folder have a subfolder for each chromosome, and in that subfolder is placed the fimo.txt result", required = True)
	parser.add_argument("-ffm","--fimo_filling_mode", help="If you wish your data in  binary (is or not present) or in number (number of the characteristic). Options are \"binary\"  or \"decimal\". Default: decimal", default="decimal")
	parser.add_argument("-ffi","--fimo_filter", help="Number equal or higher of motifs in the database to consider it as a motif. Default: 20", default=20, type=int)

	parser.add_argument("-O","--output", help="path to save results by chromosome in tsv format (default: ./)", default="./")
	parser.add_argument("-S","--saving_type", help="options to save or not rare chromosomes (as chrUn or random). Options are \"yes\" or \"not\". Default: no", default="no")
	
	#parsing arguments
	args = parser.parse_args()
	
	if args.DNA_split <= 0:
		print ("The number of kb to parse dna (--DNA_split option) must be higher than 0. Exiting")
		exit()
	
	
	###################################
	##
	## getting vectors
	##
	###################################

	#Gene Vector that looks where genes are placed
	dnaVector = geneVector(args.genome, args.DNA_split, args.GTF, args.gtf_filling_mode, args.occupancy)
		
	# for CTCF
#	ctcfVector = getFeaturedVector(args.ctcfFolder, args.percentage, args.genome, args.DNA_split, args.ctcf_filling_mode, args.occupancy)
	
	#for YY1
#	yy1Vector = getFeaturedVector(args.yy1Folder, args.percentage, args.genome, args.DNA_split, args.yy1_filling_mode, args.occupancy)

	#for DNase-seq
#	dnaseqVector = getFeaturedVector(args.DHS_dnaseq_Folder, args.percentage, args.genome, args.DNA_split, args.DHS_filling_mode, args.occupancy)
		
	#for DNA methylation
	#dnaMethVector = getFeaturedVector(args.methylation_Folder, args.percentage, args.genome, args.DNA_split, args.DNA_meth_filling_mode, args.occupancy)

	#For RNA-seq
	rnaseqVector = transcriptVector(args.genome, args.GTF, args.RNA_Folder, args.DNA_split, args.RNA_filling_mode, args.occupancy)

	# for TFs
#	tfVector = tfFeaturedVector(args.tfFolder, args.percentage, args.genome, args.DNA_split, args.tf_filling_mode, args.occupancy)

	#For FIMO
#	fimoVector = FIMOVector(args.fimo_folder, args.genome, args.DNA_split, args.fimo_filling_mode, args.occupancy, args.fimo_filter)
	
	#for histone marks
#	hmVector = histoneFeaturedVector(args.histoneMarksFolder, args.percentage, args.genome, args.DNA_split, args.histoneMarks_filling_mode, args.occupancy, args.histoneMarks_by_type)


	#saving data
#	titles = ["genes","CTCF","YY1","DNase", "DNA_met", "RNA-seq", "TFs", "FIMO"]
#	vectors = [dnaVector, ctcfVector, yy1Vector, dnaseqVector, dnaMethVector, rnaseqVector, tfVector, fimoVector]
#	
#	for item in hmVector.items():
#		titles.append("HM_"+ item[0])
#		vectors.append(item[1])

	titles = ["rna"]
	vectors = [rnaseqVector]

	saveDataset(args.output, args.saving_type, titles, vectors)
	


"""
python3 main.py -g ../02_data/reference_genome/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna -cl HepG2 -s 0.5 -gtf ../02_data/reference_genome/gencode.v24.primary_assembly.annotation-tRNAs-ERCC_phiX.gtf -ctcf ../02_data/old_yellow_orange_red/HepG2/CTCF -yy1 ../02_data/old_yellow_orange_red/HepG2/YY1 -dnaseq ../02_data/old_yellow_orange_red/HepG2/DNase-seq -dname ../02_data/old_yellow_orange_red/HepG2/WGBS -r ../02_data/old_yellow_orange_red/HepG2/polyA\ RNA-seq/ -tf ../02_data/old_yellow_orange_red/HepG2/ChIP-seq -hm ../02_data/old_yellow_orange_red/HepG2/histone_marks -ff ../02_data/reference_genome/runFimo
"""
