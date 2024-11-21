f = open("Datos_Banksy.csv", "r", encoding="utf-8")
f_out = open("Datos_Banksy_corregido.csv", "w", encoding="utf-8")


for linea in f:
    linea = linea.replace(";", ",")
    f_out.write(linea)

f.close()
f_out.close()