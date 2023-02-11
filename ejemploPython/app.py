from flask import Flask, render_template, request
import urllib.request
import json
from datetime import date

fecha = date.today()
API_key = '7OeqySIO35MjJfT7'
API_secret = 'NeqrSKFMlDoaZvo6kCxSvfHzkuT4JMcw'

##################################################################################################################
#SECCIÓN EN LA QUE SE EXTRAEN Y SE MODIFICAN LOS DATOS DE LA CLASIFICACIÓN DE LA API PARA TRATARLOS ADECUADAMENTE#

url = f'https://livescore-api.com/api-client/competitions/standings.json?competition_id=3&key={API_key}&secret={API_secret}'
response = urllib.request.urlopen(url)
contenido = response.read()
contenidoJSON = json.loads(contenido)
diccionarioDatos =contenidoJSON['data']
listaClasificacion = diccionarioDatos['table']

############################################## FIN SECCION #####################################################
#SECCIÓN EN LA QUE SE EXTRAEN Y SE MODIFICAN LOS DATOS DE LA CLASIFICACIÓN DE LA API PARA TRATARLOS ADECUADAMENTE#


################################################################################################################
#######SECCIÓN DE LAS FUNCIONES NECESARIAS PARA HACER LAS PREDICCIONES Y EL TRATAMIENTO DE DATOS CORRECTO#######

#Funcion para calcular el mes y año correcto a la fecha desde la que vamos a empezar a buscar la racha de partidos
def calculaFechaAnterior(fecha):
    mesActual = fecha.month
    mesPasado = mesActual-1
    anio = fecha.year
    if mesPasado == 0:
        mesPasado = 12
        anio = fecha.year -1

    fechaAnterior = fecha.replace(month=mesPasado)
    fechaAnterior = fechaAnterior.replace(year=anio)
    return fechaAnterior

#Funcion encargada de asignar el ID correcto al equipo seleccionado y obtener los datos de los partidos jugados en el ultimo mes
def obtenPartidos(equipo):
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

    fechaAnterior = calculaFechaAnterior(fecha)#Obtenemos de la funcion auxiliar la fecha a partir de la cual vamos a buscar los partidos
    url = f'http://livescore-api.com/api-client/scores/history.json?key={API_key}&secret={API_secret}&team={idEquipo}&competition_id=3&from={fechaAnterior}&to={fecha}'
    response = urllib.request.urlopen(url)
    contenido = response.read()
    contenidoJSON = json.loads(contenido)
    diccionarioDatos =contenidoJSON['data']
    listaDatosPartidos = diccionarioDatos['match']
    return listaDatosPartidos


#Función que crea la racha del equipo segun los partidos jugados en el ultimo mes
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

#Funcion que genera la puntuación de cada equipo segun los puntos en la clasificacion, los goles a favor, goles en contra y la puntuacion de su racha
def puntuacion(equipo):
    i = 0
    datosPartidos = obtenPartidos(equipo)
    puntRacha = float(creaRacha(equipo, datosPartidos))
    while i<len(listaClasificacion):
        if listaClasificacion[i].get('name') == equipo:
            puntos = int(listaClasificacion[i].get('points'))
            golesFavor = int(listaClasificacion[i].get('goals_scored'))
            golesContra = int(listaClasificacion[i].get('goals_conceded'))
            break
        i += 1
    puntuacionFinal = puntos + golesFavor + golesContra + puntRacha
    return puntuacionFinal

############################################## FIN SECCION #####################################################
#######SECCIÓN DE LAS FUNCIONES NECESARIAS PARA HACER LAS PREDICCIONES Y EL TRATAMIENTO DE DATOS CORRECTO#######


################################################################################################################
#######################################SECCIÓN DEL DESARROLLO DE LA WEB#########################################
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/puntos", methods=['POST'])
def funcPredecir():    
    equipoLocal = str(request.form['equipoLocal'])
    equipoVisitante = str(request.form['equipoVisitante'])

    puntuacionLocal = puntuacion(equipoLocal) # Hay que añadirle algun punto por jugar de local
    puntuacionVisitante = puntuacion(equipoVisitante)

    diferenciaPuntos = puntuacionLocal - puntuacionVisitante
    puntosAbsolutos = abs(diferenciaPuntos)

    #Hay que crear una excepción para que de error en caso de se seleccione dos veces el mismo equipo

    if puntosAbsolutos<10:
        return render_template('index.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} terminará en EMPATE.')
    else:
        if puntuacionLocal>puntuacionVisitante:
            return render_template('index.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} lo GANARÁ el {equipoLocal} jugando como local.')
        else:
            return render_template('index.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} lo GANARÁ el {equipoVisitante} jugando como visitante.')
    
    

@app.route("/racha", methods=['POST'])
def paginaRacha():
    return render_template('templateRacha.html')

@app.route("/racha-calculada", methods=['POST'])
def calculaRacha():
    equipo = str(request.form['equipoLocal'])
    ultimosPartidos = obtenPartidos(equipo)
    rachaLocal = creaRacha(equipo,ultimosPartidos)
    return render_template('templateRacha.html', racha_texto = f'La puntuación del {equipo} según los partidos jugados en el ultimo mes es de {rachaLocal}.')

if __name__ == "__main__":
    app.run()

############################################## FIN SECCION #####################################################
#######################################SECCIÓN DEL DESARROLLO DE LA WEB#########################################
