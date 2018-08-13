import pandas as pd

def saveDataset(output, saving_type, titles, vectors):
	chrs = []
	#getting chrs
	for item in vectors[0].items():
		toSave =True
		if saving_type == "no":
			if "chrUn" in item[0] or "random" in item[0]:
				toSave = False
		if toSave == True:
			chrs.append(item[0])
	
	for chr in chrs:
		dictio = {}
		i=0
		for vector in vectors:
			dictio[titles[i]] = vector[chr]
			i += 1
		df = pd.DataFrame(dictio)
		df.to_csv(output+"chr_"+chr+".tsv", sep="\t")
		
if __name__=="__main__":
	print("Use this script as a lib only")
