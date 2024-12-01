import csv
f = open("Datos_Banksy.csv", "r", encoding="utf-8")
f_out = open("main_obras.csv", "w", encoding="utf-8")
f_out.write("Titulo;Latitude;Longitude;Ubicación;Pais;Continente;Anio;Motivo;Valor;Tecnica;Estado;Imagen;Texto\n")

for linea in csv.DictReader(f, delimiter=";"):
    print(linea)
    if linea["Texto"] != "":
        f_out.write(f"{linea['Titulo']};{linea['Latitude']};{linea['Longitude']};{linea['Ubicación']};{linea['Pais']};{linea['Continente']};{linea['Anio']};{linea['Motivo']};{linea['Valor']};{linea['Tecnica']};{linea['Estado']};{linea['Imagen']};{linea['Texto']}\n")

f.close()
f_out.close()