import platform
file = open("salida_script00","r")
data = []
for line in file:
	if line not in data:
		data.append(line)
	
salida = open("clean_salida_script00","w")
for line in data:
	salida.write(line)
