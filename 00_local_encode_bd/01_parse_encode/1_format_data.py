import platform
file = open("clean_salida_script00","r")
print("use encode;")
data = []

for line in file:
	data.append(line[:-1].split("\t"))
	
#looping data to get assemblies
assemblies = []
biosamples = {}
organism = []
project = []
status = []
internal_status = []
type_experiment = []
for item in data:
	#print (item)
	#getting assemblies
	for assembly in (item[7].replace("[","").replace("u'","").replace("\'","").replace(" ","").replace("]","").split(",")):
		if assembly not in assemblies:
			assemblies.append(assembly)
			
	#getting biosample and biosample_term_name
	if item[1] not in biosamples:
		biosamples[item[1].replace("'","_")] = [item[2].replace("'","\'")]
	else:
		aux = biosamples[item[1]]
		if item[2] not in aux:
			aux.append(item[2].replace("'","_"))
			biosamples[item[1]] = aux

	#getting organism
	if item[3] not in organism:
		organism.append(item[3].replace("'","_"))

		
	#getting type of experiment
	if item[4] not in type_experiment:
		type_experiment.append(item[4].replace("\'",""))

	#getting project
	if (item[13]) not in project:
		project.append(item[13].replace("'","_"))
	
	#getting status
	if item[8] not in status:
		status.append(item[8].replace("'","_"))
	
	#getting internal status
	if item[9] not in internal_status:
		internal_status.append(item[9].replace("'","_"))

#printing commands for mysql
#type_exp
for exp in type_experiment:
	print("insert into experiment_type values ('"+str(type_experiment.index(exp))+"','"+exp+"');")
#assembly
for assembly in assemblies:
	print("insert into assembly values ('"+assembly+"');")

#project
for proj in project:
	print("insert into project values ("+str(project.index(proj))+",'"+proj+"');")

#organism
for org in organism:
	print("insert into organism values ("+str(organism.index(org))+",'"+org+"');")

#status
for stat in status:
	print("insert into status values ("+str(status.index(stat))+",'"+stat+"');")

#internal status
for stat in internal_status:
	print("insert into internal_status values ("+str(internal_status.index(stat))+",'"+stat+"');")

#biosample
i = 0
j =0
biosample_dict = {}
biosample_term_name_dict = {}
for biosample in biosamples:
	
	print("insert into biosample values ("+str(i)+",'"+biosample+"');")
	biosample_dict[biosample] = str(i)
	#for biosample term name
	
	for item in biosamples[biosample]:
		biosample_term_name_dict[item] = str(j)
		print ("insert into biosample_term_name values ("+str(j)+",'"+item.replace("'","_")+"',"+str(i)+");")
		j += 1
	i += 1
	
for item in data:
	#filling experiment table

	id = item[0]
	biosample_term_name_id = biosample_term_name_dict[item[2].replace("'","_")]
	date_created = "'"+item[5][:10]+"'"
	if date_created == "'-'":
		date_created = "NULL"
	date_released = "'"+item[6][:10]+"'"
	if date_released == "'-'":
		date_released = "NULL"
	print ("insert into experiment values ('"+id+"',"+biosample_term_name_id+","+str(type_experiment.index(item[4].replace("\'","")))+","+str(organism.index(item[3]))+","+str(project.index(item[13]))+","+str(status.index(item[8]))+","+str(internal_status.index(item[9]))+","+str(date_created)+","+str(date_released)+",'"+item[11].replace("'","_")+"','"+item[10].replace("'","_")+"','"+item[12].replace("'","_")+"',"+item[14].replace("'","_")+","+item[15].replace("'","_")+","+item[16].replace("'","_")+","+item[17].replace("'","_")+",'"+item[18]+"');")
	
for item in data:
	id = item[0]
	#filling experiment has assembly
	for assembly in (item[7].replace("[","").replace("u'","").replace("\'","").replace(" ","").replace("]","").split(",")):
		print ("insert into experiment_has_assembly values ('"+id+"','"+assembly+"');")

	

	

#print (assemblies)
#print (biosamples)
#print(organism)
#print(project)
#print(internal_status)
	
