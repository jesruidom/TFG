import urllib.request
import json
from datetime import date

fecha = date.today()
API_key = 'I3wwJ9cud1x2IZ1e'
API_secret = 'mMPgj8wLJzEQsPHaTdHCnT7BVFDDEES0'

def rachaPersonalizada(equipo, fechaInicio, fechaFin):
    if equipo == 'Almeria':
        idEquipo = 287
    elif equipo == 'Athletic Bilbao':
        idEquipo = 24
    elif equipo == 'Atletico Madrid':
        idEquipo = 26
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

    url = f'http://livescore-api.com/api-client/scores/history.json?key={API_key}&secret={API_secret}&team={idEquipo}&competition_id=3&from={fechaFin}&to={fechaInicio}'
    response = urllib.request.urlopen(url)
    contenido = response.read()
    contenidoJSON = json.loads(contenido)
    diccionarioDatos =contenidoJSON['data']
    listaDatosPartidos = diccionarioDatos['match']

    listaPartidos = listaDatosPartidos

    racha = 0
    i = 0
    victorias = 0
    empates = 0
    derrotas = 0
    numPartidos = len(listaPartidos)
    while i<numPartidos:
        resultadoTemporal = listaPartidos[i]['ft_score']
        golesLocal =  int(resultadoTemporal[0])
        golesVisitante =  int(resultadoTemporal[4])

        if golesLocal == golesVisitante:
            racha += 0.5
            empates += 1
        elif golesLocal > golesVisitante:
            if equipo == listaPartidos[i]['home_name']:
                racha += 1
                victorias += 1
            else:
                derrotas += 1
        elif golesLocal < golesVisitante:
            if equipo == listaPartidos[i]['away_name']:
                racha += 1
                victorias += 1
            else: derrotas += 1
        i += 1
    return racha, victorias, empates, derrotas, numPartidos


equipo = 'Sevilla'
fechaInicio = fecha
fechaAnterior = fecha.replace(month=1)

print(rachaPersonalizada(equipo, fechaInicio, fechaAnterior))

print(f'el valor de la racha es de {rachaPersonalizada(equipo, fechaInicio, fechaAnterior)[4]}')
print(f'el tipo del valor de la racha es {type(rachaPersonalizada(equipo, fechaInicio, fechaAnterior)[4])}')



