from flask import Flask, render_template, request
import urllib.request
import json
from datetime import date

fecha = date.today()
API_key = 'djgoa61LyiiPBT3E'
API_secret = 'izA1NKQSRw41PEN2X3r7asSILbxm4B1n'

##################################################################################################################
#SECCIÓN EN LA QUE SE EXTRAEN Y SE MODIFICAN LOS DATOS DE LA CLASIFICACIÓN DE LA API PARA TRATARLOS ADECUADAMENTE#

def extraeDatos():
    url = f'https://livescore-api.com/api-client/competitions/standings.json?competition_id=3&key={API_key}&secret={API_secret}'
    response = urllib.request.urlopen(url)
    contenido = response.read()
    contenidoJSON = json.loads(contenido)
    diccionarioDatos =contenidoJSON['data']
    listaClasificacion = diccionarioDatos['table']
    return listaClasificacion

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

    fechaAnterior = calculaFechaAnterior(fecha)#Obtenemos de la funcion auxiliar la fecha a partir de la cual vamos a buscar los partidos
    url = f'http://livescore-api.com/api-client/scores/history.json?key={API_key}&secret={API_secret}&team={idEquipo}&competition_id=3&from={fechaAnterior}&to={fecha}'
    response = urllib.request.urlopen(url)
    contenido = response.read()
    contenidoJSON = json.loads(contenido)
    diccionarioDatos =contenidoJSON['data']
    listaDatosPartidos = diccionarioDatos['match']
    return listaDatosPartidos

#Función que devuelve el numero de goles a favor que ha marcado el equipo con mas goles a favor de la clasificacion
def golesFavorMax(listaClasificacion):
    i = 0
    num = 0
    while i<len(listaClasificacion):
        if int(listaClasificacion[i].get('goals_scored')) > num:
            num = int(listaClasificacion[i].get('goals_scored'))
        i += 1
    return int(num)

#Función que devuelve el numero de goles a favor que ha recibido el equipo con mas goles en contra de la clasificacion
def golesContraMax(listaClasificacion):
    i = 0
    num = 0
    while i<len(listaClasificacion):
        if int(listaClasificacion[i].get('goals_conceded')) > num:
            num = int(listaClasificacion[i].get('goals_conceded'))
        i += 1
    return int(num)

#Función que crea la racha del equipo segun los partidos jugados en el ultimo mes
def creaRacha(equipo, listaPartidos):
    racha = 0
    i = 0
    victorias = 0
    empates = 0
    derrotas = 0
    while i<len(listaPartidos):
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
    return racha, victorias, empates, derrotas

#Funcion que genera la puntuación de cada equipo segun los puntos en la clasificacion, los goles a favor, goles en contra y la puntuacion de su racha
def puntuacion(equipo):
    i = 0
    listaClasificacion = extraeDatos()
    datosPartidos = obtenPartidos(equipo)
    numPartidosJugadosUltimoMes = len(datosPartidos)
    puntRacha = float(creaRacha(equipo, datosPartidos)[0])
    
    maximosGolesFavor = golesFavorMax(listaClasificacion)
    maximosgolesContra = golesContraMax(listaClasificacion)
    while i<len(listaClasificacion):
        if listaClasificacion[i].get('name') == equipo:
            puesto = int(listaClasificacion[i].get('rank'))
            golesFavor = int(listaClasificacion[i].get('goals_scored'))
            golesContra = int(listaClasificacion[i].get('goals_conceded'))
            break
        i += 1
    puestoEquilibrado = 21 - puesto
    puntuacionFinal = puestoEquilibrado/20 * 0.35 + golesFavor/maximosGolesFavor * 0.15 - golesContra/maximosgolesContra * 0.15 + puntRacha/numPartidosJugadosUltimoMes * 0.35
    return puntuacionFinal

def puntuacionPersonalizada(equipo, numJornada):
    with open(f'./TFG WorkSpace/jornadas/jornada{numJornada}.json') as file:
        i = 0
        dataPersonalizado = json.load(file)    
        diccionarioDatosPersonalizado = dataPersonalizado['data']
        listaClasificacionPersonalizada = diccionarioDatosPersonalizado['table']

        maximosGolesFavor = golesFavorMax(listaClasificacionPersonalizada)
        maximosgolesContra = golesContraMax(listaClasificacionPersonalizada)

        while i<len(listaClasificacionPersonalizada):
            if listaClasificacionPersonalizada[i].get('name') == equipo:
                puesto = int(listaClasificacionPersonalizada[i].get('rank'))
                golesFavor = int(listaClasificacionPersonalizada[i].get('goals_scored'))
                golesContra = int(listaClasificacionPersonalizada[i].get('goals_conceded'))
                break
            i += 1    
    puestoEquilibrado = 21 - puesto
    puntuacionFinal = puestoEquilibrado/20 * 0.45 + golesFavor/maximosGolesFavor * 0.275 - golesContra/maximosgolesContra * 0.275 #Hay que eliminar la racha ya que no se puede obtener de estos datos
    return puntuacionFinal

############################################## FIN SECCION #####################################################
#######SECCIÓN DE LAS FUNCIONES NECESARIAS PARA HACER LAS PREDICCIONES Y EL TRATAMIENTO DE DATOS CORRECTO#######


################################################################################################################
#######################################SECCIÓN DEL DESARROLLO DE LA WEB#########################################
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('paginaPrincipal.html')

@app.route("/predecir", methods=['POST'])
def paginaPredecir():
    return render_template('templatePrediccion.html')

@app.route("/prediccion-realizada", methods=['POST'])
def funcPredecir():    
    equipoLocal = str(request.form['equipoLocal'])
    equipoVisitante = str(request.form['equipoVisitante'])
    
    puntuacionLocal = puntuacion(equipoLocal) + 0.15 # Hay que añadirle algun punto por jugar de local
    puntuacionVisitante = puntuacion(equipoVisitante)

    diferenciaPuntos = puntuacionLocal - puntuacionVisitante
    puntosAbsolutos = abs(diferenciaPuntos)
#Hay que crear una excepción para que de error en caso de se seleccione dos veces el mismo equipo
    if equipoLocal == equipoVisitante:
        return render_template('templateError.html', error = f'ERROR',
                               texto_de_error = f'Has elegido dos veces el mismo equipo, vuelve a elegir para predecir el partido!')
    else:
        if puntosAbsolutos <= 0.15:
            return render_template('templatePrediccion.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} terminará en EMPATE.',
                                puntos_local = f'La puntuación del {equipoLocal} es: {puntuacionLocal}',
                                puntos_visitante = f'La puntuación del {equipoVisitante} es: {puntuacionVisitante}')
        else:
            if puntuacionLocal>puntuacionVisitante:
                return render_template('templatePrediccion.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} lo GANARÁ el {equipoLocal} jugando como local.',
                                puntos_local = f'La puntuación del {equipoLocal} es: {puntuacionLocal}',
                                puntos_visitante = f'La puntuación del {equipoVisitante} es: {puntuacionVisitante}')
            else:
                return render_template('templatePrediccion.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} lo GANARÁ el {equipoVisitante} jugando como visitante.',
                                puntos_local = f'La puntuación del {equipoLocal} es: {puntuacionLocal}',
                                puntos_visitante = f'La puntuación del {equipoVisitante} es: {puntuacionVisitante}')
            
            
@app.route("/predecir-personalizado", methods=['POST'])
def paginaPredecirPersonalizada():
    return render_template('templatePrediccionPersonalizada.html')  

@app.route("/prediccion-personalizada-realizada", methods=['POST'])
def funcPredecirPersonalizada():  
    numJornada = int(request.form['numJornada'])  
    equipoLocal = str(request.form['equipoLocal'])
    equipoVisitante = str(request.form['equipoVisitante'])

    puntuacionLocal = puntuacionPersonalizada(equipoLocal, numJornada) + 0.15 # Hay que añadirle algun punto por jugar de local
    puntuacionVisitante = puntuacionPersonalizada(equipoVisitante,numJornada)

    diferenciaPuntos = puntuacionLocal - puntuacionVisitante
    puntosAbsolutos = abs(diferenciaPuntos)
#Hay que crear una excepción para que de error en caso de se seleccione dos veces el mismo equipo
    if equipoLocal == equipoVisitante:
        return render_template('templateError.html', error = f'ERROR',
                               texto_de_error = f'Has elegido dos veces el mismo equipo, vuelve a elegir para predecir el partido!')
    else:
        if puntosAbsolutos <= 0.15:
            return render_template('templatePrediccionPersonalizada.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} terminará en EMPATE.',
                                puntos_local = f'La puntuación del {equipoLocal} es: {puntuacionLocal}',
                                puntos_visitante = f'La puntuación del {equipoVisitante} es: {puntuacionVisitante}')
        else:
            if puntuacionLocal>puntuacionVisitante:
                return render_template('templatePrediccionPersonalizada.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} lo GANARÁ el {equipoLocal} jugando como local.',
                                puntos_local = f'La puntuación del {equipoLocal} es: {puntuacionLocal}',
                                puntos_visitante = f'La puntuación del {equipoVisitante} es: {puntuacionVisitante}')
            else:
                return render_template('templatePrediccionPersonalizada.html', puntos_texto = f'El partido entre el {equipoLocal} y el {equipoVisitante} lo GANARÁ el {equipoVisitante} jugando como visitante.',
                                puntos_local = f'La puntuación del {equipoLocal} es: {puntuacionLocal}',
                                puntos_visitante = f'La puntuación del {equipoVisitante} es: {puntuacionVisitante}')

@app.route("/racha", methods=['POST'])
def paginaRacha():
    return render_template('templateRacha.html')

@app.route("/racha-calculada", methods=['POST'])
def calculaRacha():
    equipo = str(request.form['equipoLocal'])
    ultimosPartidos = obtenPartidos(equipo)
    rachaLocal = creaRacha(equipo,ultimosPartidos)
    return render_template('templateRacha.html', racha_texto = f'El {equipo} ha jugado {len(ultimosPartidos)} partidos en el último mes, ha ganado {rachaLocal[1]}, empatado {rachaLocal[2]} y perdido {rachaLocal[3]}.', 
        racha_texto2 = f'Por tanto, ha obteniendo una puntuación de {rachaLocal[0]}.')

@app.route("/documentacion", methods=['POST'])
def paginaDocumentacion():
    return render_template('templateDocumentacion.html')

if __name__ == "__main__":
    app.run()

############################################## FIN SECCION #####################################################
#######################################SECCIÓN DEL DESARROLLO DE LA WEB#########################################
