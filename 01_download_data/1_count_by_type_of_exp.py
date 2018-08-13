import sys
file = open(sys.argv[1],"r")

dictio = {}
print ("Este script te ayuda a decidir que lineas celulares bajar. ejemplo python 1_count_by...py salida.tsv")
for line in file:
	if "GRCh38" in line:	
		aux = line[:-1].split("\t")
		
		if aux[3] in dictio:
			if aux[1] in dictio[aux[3]]:
				dictio[aux[3]][aux[1]] += 1
			else:
				dictio[aux[3]][aux[1]] = 1
		else:
			dictio[aux[3]] = {aux[1]:1}


for item in dictio.items():
	hip_sites = False
	prot_dna = False
	dna_meth = False
	rna = False
	suma = 0
	for item2 in item[1].items():
		if item2[0] == "DNase-seq" or item2[0] == "FAIRE-seq" or item2[0] == "ATAC-seq":
			hip_sites = True
			suma += item2[1]
		if item2[0] =="ChIP-seq":
			prot_dna = True
			suma += item2[1]
		if item2[0] == "WGBS" or item2[0] == "RRBS" or item2[0] == "methyl array":
			dna_meth = True			
			suma += item2[1]
		if item2[0] == "polyA RNA-seq":
			suma += item2[1]
			rna = True
			
	if hip_sites == True and prot_dna == True and dna_meth == True and rna == True:
		print(item[0]+"\t"+str(item[1])+"\t"+str(suma)+"\n")
