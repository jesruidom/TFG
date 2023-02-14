import urllib.request
import json
from datetime import date

fecha = date.today()
API_key = '7OeqySIO35MjJfT7'
API_secret = 'NeqrSKFMlDoaZvo6kCxSvfHzkuT4JMcw'

#Funcion para calcular el mes y año correcto a la fecha desde la que vamos a empezar a buscar la racha de partidos
def calculaFechaAnterior(fecha):
    mesActual = fecha.month
    mesPasado = mesActual-1
    anio = fecha.year
    if mesPasado == 0:
        mesPasado = 12
        anio = fecha.year -1
    return mesPasado, anio

#Obtenemos el mes anteior para sustituirlo en la llamada a la API y pedir los resultados a partir de un mes anteior
datosFechaAnterior = calculaFechaAnterior(fecha)
fechaAnterior = fecha.replace(month=datosFechaAnterior[0])
fechaAnterior = fechaAnterior.replace(year=datosFechaAnterior[1])

#Funcion que busca y devuelve la lectura de la API de los partidos jugados por el equipo solicitado en el ultimo mes
def buscaRacha(equipo):    
    if equipo == 'Almeria':
        idEquipo = 287
    elif equipo == 'Athletic Bilbao':
        idEquipo = 24
    elif equipo == 'Atletico Madrid':
        idEquipo = 43
    elif equipo == 'Barcelona':
        idEquipo = 21
    elif equipo == 'Cadiz':
        idEquipo = 798
    elif equipo == 'Celta Vigo':
        idEquipo = 32
    elif equipo == 'Elche':
        idEquipo = 1309
    elif equipo == 'Espanyol':
        idEquipo = 38
    elif equipo == 'Getafe':
        idEquipo = 30
    elif equipo == 'Girona':
        idEquipo = 31
    elif equipo == 'Mallorca':
        idEquipo = 1814
    elif equipo == 'Osasuna':
        idEquipo = 794
    elif equipo == 'Rayo Vallecano':
        idEquipo = 792
    elif equipo == 'Real Betis':
        idEquipo = 35
    elif equipo == 'Real Madrid':
        idEquipo = 27
    elif equipo == 'Real Sociedad':
        idEquipo = 22
    elif equipo == 'Sevilla':
        idEquipo = 23
    elif equipo == 'Valencia':
        idEquipo = 29
    elif equipo == 'Valladolid':
        idEquipo = 235
    elif equipo == 'Villarreal':
        idEquipo = 33

    url = f'http://livescore-api.com/api-client/scores/history.json?key={API_key}&secret={API_secret}&team={idEquipo}&competition_id=3&from={fechaAnterior}&to={fecha}'
    infoRacha = urllib.request.urlopen(url)
    return infoRacha

#Obtenemos los datos de los partidos jugados por el equipo solicitado en el ultimo mes
equipo = 'Sevilla'
response = buscaRacha(equipo)

#Procesado de los datos proporcionados por la API hasta dejarlos en forma de lista con los partidos jugados
contenido = response.read()
contenidoJSON = json.loads(contenido)
diccionarioDatos =contenidoJSON['data']
listaDatosPartidos = diccionarioDatos['match']

#Parte del codigo para mostrar cada linea de la lista
'''i = 0
while i<len(listaClasificacion):
    print(listaClasificacion[i])
    i += 1'''


#Los datos necesarios para tratar la racha de puntos son home_name, away_name y ft_score
#Parte del codigo para probar los resultados de un equipo en el ultimo mes

print(f'Estamos buscando los partidos jugados por el {equipo} entre los dias {fechaAnterior} y {fecha}\n')
j = 0
while j<len(listaDatosPartidos):
    print('El partido entre el ',listaDatosPartidos[j]['home_name'], 'y el', listaDatosPartidos[j]['away_name'], 'terminó con un resultado de:', listaDatosPartidos[j]['ft_score'])
    j += 1


print("\n----------------------------------------------------------\n")

tipoResultados = type(listaDatosPartidos[0]['ft_score'])
resultadoDePrueba = listaDatosPartidos[0]['ft_score']
print(f'Vamos a analizar el dato {resultadoDePrueba}')
print(f'El primer valor del dato a analizar es: {resultadoDePrueba[0]} y es de tipo {type(resultadoDePrueba[0])} pero lo podemos pasar a tipo int mediante {type(int(resultadoDePrueba[0]))}')
print(f'El primer valor del dato a analizar es: {resultadoDePrueba[4]} y es de tipo {type(resultadoDePrueba[4])} pero lo podemos pasar a tipo int mediante {type(int(resultadoDePrueba[4]))}')

def creaRacha(equipo, listaPartidos):
    racha = 0
    i = 0
    while i<len(listaPartidos):
        resultadoTemporal = listaPartidos[i]['ft_score']
        golesLocal =  int(resultadoTemporal[0])
        golesVisitante =  int(resultadoTemporal[4])
        if golesLocal == golesVisitante:
            racha += 0.5
        elif golesLocal > golesVisitante:
            if equipo == listaPartidos[i]['home_name']:
                racha += 1
        elif golesLocal < golesVisitante:
            if equipo == listaPartidos[i]['away_name']:
                racha += 1
        else:
            racha += 0
        i += 1
    return racha

rachaAcomulada = creaRacha(equipo, listaDatosPartidos)
#print(f'La racha acomulada del {equipo} es de {rachaAcomulada}')

