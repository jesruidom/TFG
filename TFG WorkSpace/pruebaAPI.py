import urllib.request
import json

API_key = 'djgoa61LyiiPBT3E'
API_secret = 'izA1NKQSRw41PEN2X3r7asSILbxm4B1n'

#url = 'https://livescore-api.com/api-client/competitions/standings.json?competition_id=3&key=7OeqySIO35MjJfT7&secret=NeqrSKFMlDoaZvo6kCxSvfHzkuT4JMcw'
url = f'https://livescore-api.com/api-client/competitions/standings.json?competition_id=3&key={API_key}&secret={API_secret}'
response = urllib.request.urlopen(url)
print("La variable response es de tipo: ",type(response))
contenido = response.read()
print("La variable contenido es de tipo: ",type(contenido))
#contenidoString = contenido.decode()
#print("La variable contenidoString es de tipo: ",type(contenidoString))
#print(contenido)
#contenidoJSON = json.loads(contenidoString)
contenidoJSON = json.loads(contenido)
print("La variable contenidoJSON es de tipo: ",type(contenidoJSON), '\n')
print("Se han obtenido los datos de la API en formato JSON pudiendo ser tratados como un diccionario")
print("Las claves del diccionario contenidoJSON son:",contenidoJSON.keys())
#print("Contenido de la clave 'success' en contenidoJSON",contenidoJSON['success'])
diccionarioDatos = contenidoJSON['data']
print("Contenido de la clave 'data' en contenidoJSON",diccionarioDatos.keys())
listaClasificacion = diccionarioDatos['table']
print("El contenido de la clave 'table' en contenidoJSON es una lista con los datos de la clasificacion y se muestra de la siguiente forma:", '\n')
print("Datos de la clasificación:")
i = 0
while i<len(listaClasificacion):
    print(listaClasificacion[i])
    i += 1

print("Los datos de la listaClasificacion son de tipo: ", type(listaClasificacion[0]))
print("Las claves de este equipo son: ", listaClasificacion[0].keys())
#print("El equipo del indice 0 es el:", listaClasificacion[0].get('name'))

#Para obtener los datos del Barcelona hacemos lo siguiente:
'''r = listaClasificacion[0].get('name') == 'Barcelona'
print("El resultado de r es:",r)'''

#FUNCION QUE DEVUELVE LOS PUNTOS ACTUALES EN LA CLASIFICACION DEL EQUIPO SELECCIONADO
def puntLocal(equipo):
    i = 0
    while i<len(listaClasificacion):
        if listaClasificacion[i].get('name') == equipo:
            puntos = listaClasificacion[i].get('points')
            break
        i += 1
    return puntos

def devPuntuaciones(equipo):
    i = 0
    while i<len(listaClasificacion):
        if listaClasificacion[i].get('name') == equipo:
            puesto = int(listaClasificacion[i].get('rank'))
            golesFavor = int(listaClasificacion[i].get('goals_scored'))
            golesContra = int(listaClasificacion[i].get('goals_conceded'))
            break
        i += 1
    #puntuacionFinal = puesto + golesFavor - golesContra
    #return puntuacionFinal
    return puesto, golesFavor, golesContra

#puntuaciones = devPuntuaciones('Real Madrid')
#print('La funcion devPuntuaciones devuelve: ', puntuaciones)
#print(f'Y es de tipo {type(puntuaciones)}')

#Esta funcion devuelve el numero de goles a favor que ha marcado el equipo con mas goles a favor de la clasificacion
def golesFavorMax(listaClasificacion):
    i = 0
    num = 0
    while i<len(listaClasificacion):
        if int(listaClasificacion[i].get('goals_scored')) > num:
            num = int(listaClasificacion[i].get('goals_scored'))
        i += 1
    return int(num)

#print(f'La funcionn golesFavorMax devuelve el valor de goles a favor maximo: {golesFavorMax(listaClasificacion)}')

#Esta funcion devuelve el numero de goles a favor que ha recibido el equipo con mas goles en contra de la clasificacion
def golesContraMax(listaClasificacion):
    i = 0
    num = 0
    while i<len(listaClasificacion):
        if int(listaClasificacion[i].get('goals_conceded')) > num:
            num = int(listaClasificacion[i].get('goals_conceded'))
        i += 1
    return int(num)

#print(f'La funcionn golesContraMax devuelve el valor de goles en contra maximo: {golesContraMax(listaClasificacion)}')

def equilibraPuntuacion(puntuaciones):
    aux = int(21 - int(puntuaciones[0]))
    puntosEquilibrados = float(aux/20)
    golesFavorEquilibrados = float(puntuaciones[1]/golesFavorMax(listaClasificacion))
    golesContraEquilibrados = float(puntuaciones[2]/golesContraMax(listaClasificacion))
    #return puntosEquilibrados, golesFavorEquilibrados, golesContraEquilibrados
    puntuacionFinal = float(puntosEquilibrados + golesFavorEquilibrados - golesContraEquilibrados)
    return puntuacionFinal

#print(f'la funcion equilibrapuntuaciones devuelve {equilibraPuntuacion(puntuaciones)}')

def comparacion(equipoLocal, equipoVisitante):
    #puntuacionLocal = puntuacion(equipoLocal)
    puntuacionLocal = equilibraPuntuacion(devPuntuaciones(equipoLocal))
    #puntuacionVisitante = puntuacion(equipoVisitante)
    puntuacionVisitante = equilibraPuntuacion(devPuntuaciones(equipoVisitante))
    diferenciaPuntos = puntuacionLocal - puntuacionVisitante
    puntosAbsolutos = abs(diferenciaPuntos)
    if puntosAbsolutos==0:
        res = "Hay probabilidades de que el partido entre el", equipoLocal, "y el ", equipoVisitante, "termine en EMPATE"
    else:
        if puntuacionLocal > puntuacionVisitante:
            res = "El partido lo GANARA el " , equipoLocal,"con una puntuacion de", puntuacionLocal
        else:
            res = "El partido lo GANARA el", equipoVisitante,"con una puntuacion de", puntuacionVisitante, "puntuacion local: ", puntuacionLocal
    return res

equipoLocal = 'Sevilla'
equipoVisitante = 'Barcelona'
#print("El", equipoLocal, "tiene", puntLocal(equipoLocal), "puntos")
#print("El", equipoLocal, "tiene", puntLocal(equipoVisitante), "puntos")
#print("El", equipoLocal, "tiene", puntuacion(equipoLocal), "puntos")
#print("El", equipoVisitante, "tiene", puntuacion(equipoVisitante), "puntos")
print(comparacion(equipoLocal, equipoVisitante))

print("\n----------------------------------------------------------\n")
print("Puntos de control para el Sevilla: ", puntLocal(equipoLocal))

# print("El parametro points es de tipo", type(int(listaClasificacion[0].get('points'))))
# print("El parametro rank es de tipo", type(float(listaClasificacion[0].get('rank'))))
# print("El parametro goal_diff es de tipo", type(float(listaClasificacion[0].get('goal_diff'))))
# print("El parametro won es de tipo", type(float(listaClasificacion[0].get('won'))))
# print("El parametro drawn es de tipo", type(float(listaClasificacion[0].get('drawn'))))
# print("El parametro lost es de tipo", type(float(listaClasificacion[0].get('lost'))))
