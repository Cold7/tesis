"""
A tool to create vector of zeros starting from a genome

Module that read a genome file in fasta format and return a matrix of zeros, where its lenght is given by lenght of genome divided by kb to split. For more information please write to contrerasriquelme.sebastian@gmail.com
"""
import numpy as np
import math
from Bio import SeqIO
from math import ceil

def get_vector(genome, kb):
	"""
	Function that take a genome, read it and return a dictionary of chr:[vector of zeros of upper round of length_genome/kb (with kb*1000 to know number of nucleotides) 
	"""
	dictGenome = {}
	for seq_record in SeqIO.parse(genome,"fasta"):
		dictGenome[seq_record.id] = np.zeros(int(math.ceil(len(seq_record.seq)/(kb*1000))))#round to the next int and kb * 1000 is to get pb
	return dictGenome


if __name__ == "__main__":
	print ("Use help(\"genome\") to get more information")
