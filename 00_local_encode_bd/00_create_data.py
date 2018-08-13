import multiprocessing as mp
import requests, json, collections, time

def get_errors(audit):
	
	return "there is not implementation of error"
	
def get_cellCicle_tratments_dates_internalStatus(id):
	HEADERS = {'accept': 'application/json'}	
	URL = "https://www.encodeproject.org"+id
	response = None
	while response == None:
		try:
			response = requests.get(URL, headers=HEADERS).json()
		except:
			pass
	
	date_created = "-"
	date_released = "-"
	cellCicle = "-"
	treatments = "-"
	assemblies = "-"
	internalStatus = "-"
	genetic_modifications = "-"
	rfa = "-"
	replication_type = '-'
	
	try:
		rfa = response["award"]["rfa"].encode("utf-8")
	except:
		pass
		
	try:
		replication_type = response["replication_type"].encode("utf-8")
	except:
		pass
	
	try:
		date_created = str(response["date_created"].encode('utf-8'))
	except:
		pass

	try:
		date_released = str(response["date_released"].encode('utf-8'))
	except:
		pass
	
	try:
		assemblies = response["assembly"]
	except:
		pass
	
	try:
		internalStatus = response["internal_status"].encode("utf-8")
	except:
		pass
	
	try:
		treatments = response["replicates"][0]["library"]["biosample"]["treatments"][0]["treatment_term_name"].encode('utf-8')
	except:
		pass

	try:
		cellCicle = response["replicates"][0]["library"]["biosample"]["phase"].encode("utf-8")
	except:
		pass

	try:
		genetic_modifications = response["replicates"][0]["library"]["biosample"]["genetic_modifications"][0].encode("utf-8")
	except:
		pass
		
	#searching for errors
	
	#red_errors = ["extremely low read length","extremely low read depth","extremely low coverage","inconsistent replicate","technical replicates with not identical biosample","replicate with no library","extremely low spot score","not compliant platform","not tagged antibody","inconsistent target","mismatched tag target","missing antibody","missing biosample","missing biosample_term_id","missing biosample_term_name","missing biosample type","missing donor","missing target","multiple paired_with","missing raw data in replicate","missing possible controls","mismatched control","inconsistent ontology term","inconsistent depleted_in_term length","depleted_in length mismatch","inconsistent organism","inconsistent donor","inconsistent library biosample","inconsistent paired_with","inconsistent control","inconsistent document_type","inconsistent mutated_gene organism","invalid donor mutated_gene","invalid dates","invalid possible_control","invalid depleted_in_term_id","unexpected step_run"]	
	#orange_errors = ["insufficient read length","control insufficient read depth","insufficient read depth","insufficient coverage","insufficient replicate concordance","unreplicated experiment","severe bottlenecking","insufficient library complexity","insufficient spot score","missing spikeins","missing rna fragment size","missing input control","missing run_type","not eligible antibody","partially characterized antibody","uncharacterized antibody","antibody not characterized to standard","no characterizations submitted","no primary characterizations","no secondary characterizations","need compliant primaries","need compliant secondaries","missing documents","missing controlled_by","inconsistent age","inconsistent sex"]
	#yellow_errors = ["control low read depth","low read depth","low coverage","low replicate concordance","borderline replicate concordance","mild to moderate bottlenecking","moderate library complexity","poor library complexity","low spot score","inconsistent control read length","inconsistent control run type","inconsistent control platform","inconsistent platforms","mixed read lengths","mixed run types","non-standard run_type","not compliant platform","antibody characterized with exemption","characterizations not reviewed","missing derived_from","missing genotype","missing external identifiers","inconsistent target of control experiment","missing reference","missing ihec required assay","multiple donors in reference epigenome","multiple biosample treatments in reference epigenome"]
	
	red = 0
	orange = 0
	yellow = 0
	
	errors = { "red" : {}, "orange" : {}, "yellow" : {}}
	if "audit" in response:
		if "NOT_COMPLIANT" in response["audit"]:
			for m in range(len(response["audit"]["NOT_COMPLIANT"])):
				error = response["audit"]["NOT_COMPLIANT"][m]["category"]
				if error in errors["orange"]:
					errors["orange"][error] += 1
				else:
					errors["orange"][error] = 1

		if "WARNING" in response["audit"]:
			for m in range(len(response["audit"]["WARNING"])):
				error = response["audit"]["WARNING"][m]["category"]
				if error in errors["yellow"]:
					errors["yellow"][error] += 1
				else:
					errors["yellow"][error] = 1
								
		if "ERROR" in response["audit"]:
			for m in range(len(response["audit"]["ERROR"])):
				error = response["audit"]["ERROR"][m]["category"]
				if error in errors["red"]:
					errors["red"][error] += 1
				else:
					errors["red"][error] = 1		
	red = len(errors["red"])
	orange = len(errors["orange"])
	yellow = len(errors["yellow"])
	
	#print red, orange, yellow
	#raw_input("#")
	return [date_created, date_released, assemblies, internalStatus, treatments, cellCicle, genetic_modifications, rfa, red, orange, yellow, replication_type]


URL = "https://www.encodeproject.org/matrix/?type=Experiment&x.limit="
response = None
HEADERS = {'accept': 'application/json'}
response = requests.get(URL, headers=HEADERS)
# Extract the JSON response as a python dict
response_json_dict = response.json()

i = 0
while i < len(response_json_dict["matrix"]["y"]["biosample_type"]["buckets"]):
	biosample = response_json_dict["matrix"]["y"]["biosample_type"]["buckets"][i]["key"]
#	print biosample
	j = 0
	while j < len(response_json_dict["matrix"]["y"]["biosample_type"]["buckets"][i]["biosample_term_name"]["buckets"]):
		biosample_term_name = (response_json_dict["matrix"]["y"]["biosample_type"]["buckets"][i]["biosample_term_name"]["buckets"][j]["key"])
#		print biosample_term_name
		name = biosample_term_name.replace(" ","+")
		URL2="https://www.encodeproject.org/search/?type=Experiment&biosample_term_name="+name+"&limit=all"
		#example until here: https://www.encodeproject.org/search/?type=Experiment&biosample_term_name=K562&limit=all&format=json
		response2 = False
		#print biosample_term_name
		while response2 == False:
			response2 = requests.get(URL2, headers=HEADERS).json()
			k = 0
			while k < len(response2["@graph"]):
				data = response2["@graph"][k]
				id = data["@id"]
				organism = "unknown"
				try:
					organism = data["replicates"][0]["library"]["biosample"]["organism"]["scientific_name"]
				except:
					pass
				experiment_type = data["assay_title"]
				status = "-"
				try:
					status = data["status"]
				except:
					print "# please confirm status on experiment "+id
					pass

				target = "-"
				try:
					target = data["target"]["label"]
				except:
					pass
				project = "-"
				try:
					project = data["award"]["project"]
				except:
					pass
				
				
				#getting dates, cell cicle, treatments and internalStatus
				date_created, date_released, assemblies, internalStatus, treatments, cellCicle, genetic_modifications,encodeV, red_e, orange_e, yellow_e, replication_type = get_cellCicle_tratments_dates_internalStatus(id)

				#getting number of biological samples
				l = 0
				number_of_biological_replicates = 0
				if "replicates" in  data:
					number_of_biological_replicates += len(data["replicates"])
				#print "### "+str(k)
				print str(id)+"\t"+str(biosample)+"\t"+str(biosample_term_name)+"\t"+str(organism)+"\t"+str(experiment_type)+"\t"+str(date_created)+"\t"+str(date_released)+"\t"+str(assemblies)+"\t"+str(status)+"\t"+str(internalStatus)+"\t"+str(treatments)+"\t"+str(cellCicle)+"\t"+str(genetic_modifications)+"\t"+str(encodeV)+"\t"+str(red_e)+"\t"+str(orange_e)+"\t"+str(yellow_e)+"\t"+str(number_of_biological_replicates)+"\t"+str(replication_type)
	
				k += 1
			

		j += 1

	i += 1

