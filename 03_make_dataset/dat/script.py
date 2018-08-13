file = open("HOCOMOCOv11_full_HUMAN_mono_meme_format.meme","r")
lista = []
for line in file:
	if "nsites" in line:
		nsites = int(line[:-1].split("nsites=")[-1].replace(" ",""))
		lista.append(nsites)
print (sorted(lista))
