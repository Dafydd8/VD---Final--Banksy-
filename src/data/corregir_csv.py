import csv

f = open("Datos_Banksy_valores.csv", "r", encoding="utf-8")
f2 = open("main_obras.csv", "r", encoding="utf-8")
f_out = open("Datos_Banksy_corregido.csv", "w", encoding="utf-8")
f_out.write('Titulo;Latitud;Longitud;Ubicación;Pais;Continente;Anio;Motivo;Valor;Tecnica;Estado;Imagen;Texto\n')


obras = {}
for linea in csv.DictReader(f2, delimiter=";"):
    obras[linea['Titulo']] = linea['Texto']

print(obras)

for lina in csv.DictReader(f, delimiter=";"):
    print(lina)
    if lina['\ufeffTitulo'] in obras:
        f_out.write(f"{lina['\ufeffTitulo']};{lina['Latitud']};{lina['Longitud']};{lina['Ubicación']};{lina['Pais']};{lina['Continente']};{lina['Anio']};{lina['Motivo']};{lina['Valor']};{lina['Tecnica']};{lina['Estado']};{lina['Imagen']};{obras[lina['\ufeffTitulo']]}\n")
    else:
        f_out.write(f"{lina['\ufeffTitulo']};{lina['Latitud']};{lina['Longitud']};{lina['Ubicación']};{lina['Pais']};{lina['Continente']};{lina['Anio']};{lina['Motivo']};{lina['Valor']};{lina['Tecnica']};{lina['Estado']};{lina['Imagen']};\n")
f.close()
f_out.close()
f2.close()