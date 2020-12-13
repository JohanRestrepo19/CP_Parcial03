import json

def cargarJson(ruta):
    with open(ruta) as contenido:
        informacion_json = json.load(contenido)
    contenido.close()
    return informacion_json

def main():
    ruta_json = "mapa_colision.json"
    informacion_json = cargarJson(ruta_json)
    diccionario_mapa_colision = informacion_json['layers'][0]
    ls_mapa_colision = diccionario_mapa_colision['data']
    print(ls_mapa_colision)
    limite_fila = diccionario_mapa_colision['height']
    limite_columna = diccionario_mapa_colision['width']
    contador_bloque = 0
    print(limite_fila,limite_columna)

    for fila in range(limite_fila):
        for columna in range(limite_columna):
            print(ls_mapa_colision[contador_bloque], end=' ')
            contador_bloque += 1
        print()


if __name__ == '__main__':
    main()
