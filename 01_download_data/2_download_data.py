from os import system
import requests, json
import argparse # arguments parser
import os

def download(exp_type, id, current_biosample):
	log = open("log.txt","a")
	HEADERS = {'accept': 'application/json'}	
	URL = "https://www.encodeproject.org"+id
	response = None
	while response == None:
		try:
			response = requests.get(URL, headers=HEADERS).json()
		except:
			pass

	#creating output folder if it does not exist
	current_folder = ""
	folder = id.split("/")[-2]

	if not os.path.exists("\""+output+"/"+current_biosample+"/"+exp_type+"\""):
		try: 
			os.mkdir(output+"/"+current_biosample+"/"+exp_type)
		except:
			pass
	
	if exp_type == "ChIP-seq":
		folder = response["target"]["name"]
		
	if not os.path.exists("\""+args.output+"/"+current_biosample+"/"+exp_type+"/"+folder+"\""):
		try: 
			log.write("creando carpeta "+args.output+"/"+current_biosample+"/"+exp_type+"/"+folder+"\n")
			os.mkdir(args.output+"/"+current_biosample+"/"+exp_type+"/"+folder)
			current_folder = args.output+"/"+current_biosample+"/"+exp_type+"/"+folder
		except:
			current_folder = args.output+"/"+current_biosample+"/"+exp_type+"/"+folder
			log.write("fallo en la creacion de la carpeta "+args.output+"/"+current_biosample+"/"+exp_type+"/"+folder+"\n")

	
	if exp_type == "ChIP-seq":
		data = response["files"]
		for i in range (len(data)):
			if  data[i]["output_type"] == "optimal idr thresholded peaks" and data[i]["file_format"] == "bigBed" and data[i]["assembly"] == "GRCh38" and data[i]["status"] == "released":
				#data i output_Type "optimal idr thresholded peaks"     "conservative idr thresholded peaks"				
				system("wget https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bigBed -O \""+current_folder+"/"+data[i]["accession"]+".bigBed\"")
				log.write("https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bigBed -O \""+current_folder+"/"+data[i]["accession"]+".bigBed\"\n")
				system("./bigBedToBed \""+current_folder+"/"+data[i]["accession"]+".bigBed\" \""+current_folder+"/"+data[i]["accession"]+"_optimal.bed\"" )
				system("rm \""+current_folder+"/"+data[i]["accession"]+".bigBed\"")
			
			if  data[i]["output_type"] == "conservative idr thresholded peaks" and data[i]["file_format"] == "bigBed" and data[i]["assembly"] == "GRCh38" and data[i]["status"] == "released":
				system("wget https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bigBed -O \""+current_folder+"/"+data[i]["accession"]+".bigBed\"")
				log.write("https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bigBed -O \""+current_folder+"/"+data[i]["accession"]+".bigBed\"\n")
				system("./bigBedToBed \""+current_folder+"/"+data[i]["accession"]+".bigBed\" \""+current_folder+"/"+data[i]["accession"]+"_conservative.bed\"" )
				system("rm \""+current_folder+"/"+data[i]["accession"]+".bigBed\"")

			if  data[i]["output_type"] == "replicated peaks" and data[i]["file_format"] == "bigBed" and data[i]["assembly"] == "GRCh38" and data[i]["status"] == "released":
				system("wget https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bigBed -O \""+current_folder+"/"+data[i]["accession"]+".bigBed\"")
				log.write("https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bigBed -O \""+current_folder+"/"+data[i]["accession"]+".bigBed\"\n")
				system("./bigBedToBed \""+current_folder+"/"+data[i]["accession"]+".bigBed\" \""+current_folder+"/"+data[i]["accession"]+"_conservative.bed\"" )
				system("rm \""+current_folder+"/"+data[i]["accession"]+".bigBed\"")


	elif exp_type == "WGBS":
		data = response["files"]
		for i in range (len(data)):
			if data[i]["output_type"] == "methylation state at CpG" and data[i]["file_format"] == "bed" and data[i]["assembly"] == "GRCh38" and data[i]["status"] == "released":
				system("wget https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bed.gz -O \""+current_folder+"/"+data[i]["accession"]+".bed.gz\"")
				system("gunzip \""+current_folder+"/"+data[i]["accession"]+".bed.gz\"")

	elif exp_type == "polyA RNA-seq":
		data = response["files"]
		for i in range (len(data)):
			if data[i]["output_type"] == "gene quantifications" and data[i]["file_format"] == "tsv" and data[i]["assembly"] == "GRCh38" and data[i]["status"] == "released":
				try:
					system("wget https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".tsv -O \""+current_folder+"/"+data[i]["accession"]+"_gene.tsv\"")
				except:
					pass
			if data[i]["output_type"] == "transcript quantifications" and data[i]["file_format"] == "tsv" and data[i]["assembly"] == "GRCh38" and data[i]["status"] == "released":
				try:
					system("wget https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".tsv -O \""+current_folder+"/"+data[i]["accession"]+"_transcript.tsv\"")
				except:
					pass					
	else:
		data = response["files"]
		for i in range (len(data)):
			if data[i]["file_type"] == "bed narrowPeak" and data[i]["file_format"] == "bed" and data[i]["assembly"] == "GRCh38" and data[i]["status"] == "released":
				system("wget https://www.encodeproject.org/files/"+data[i]["accession"]+"/@@download/"+data[i]["accession"]+".bed.gz -O \""+current_folder+"/"+data[i]["accession"]+".bed.gz\"")
				system("gunzip \""+current_folder+"/"+data[i]["accession"]+".bed.gz\"")
	log.close()
if __name__=="__main__":
	global output
	parser = argparse.ArgumentParser()
	parser.add_argument("-B", "--biosample_file_name", help="File with Biosample names to download associated data", required=True)
	parser.add_argument("-Q", "--query", help="Query file result from a query to the encode database in tsv format", required=True)
	parser.add_argument("-O", "--output", help="Output folder to download data", required=True)
	args = parser.parse_args()
	
	#creating output folder if it does not exist
	if not os.path.exists(args.output):
		try: 
			os.mkdir(args.output)
		except:
			print ("Can not create directory "+args.output+". exiting")
			exit(1)
	
	output = args.output
	biosample_filename = open(args.biosample_file_name)
	for line in biosample_filename:
		current_biosample = line[:-1]		
		#creating output folder if it does not exist
		if not os.path.exists(args.output+"/"+current_biosample):
			try: 
				os.mkdir(args.output+"/"+current_biosample)
			except:
				print ("Can not create directory "+args.output+"/"+current_biosample+". exiting")
				exit(1)		
		dataFile = open(args.query,"r")
		for line in dataFile:
			aux = line[:-1].split("\t")
			if aux[3] == current_biosample:
				if aux[1] == "DNase-seq":
					download("DNase-seq",aux[0],current_biosample)
				if aux[1] == "ChIP-seq":
					download("ChIP-seq", aux[0],current_biosample)
				if aux[1] == "WGBS":
					download("WGBS", aux[0], current_biosample)
				if aux[1] == "polyA RNA-seq":
					download("polyA RNA-seq", aux[0], current_biosample)
		dataFile.close()
	biosample_filename.close()

"""
"""
