import platform
file = open("datos_formateados.sql","r")
data = []
for line in file:
	aux = 0
	for item in data:
		if item == line:
			aux = 1
	if aux==0:
		data.append(line)
	#if line not in data:
	#	data.append(line)

	
salida = open("clean_datos_formateados.sql","w")
for line in data:
	salida.write(line)
