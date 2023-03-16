import json

def puntuacionPersonalizada(equipo, numJornada):
    if numJornada == 20:
        with open('./TFG WorkSpace/jornadas/jornada20.json') as file:
            i = 0
            dataPersonalizado = json.load(file)    
            diccionarioDatosPersonalizado = dataPersonalizado['data']
            listaClasificacionPersonalizada = diccionarioDatosPersonalizado['table']
            while i<len(listaClasificacionPersonalizada):
                if listaClasificacionPersonalizada[i].get('name') == equipo:
                    puntos = int(listaClasificacionPersonalizada[i].get('points'))
                    break
                i += 1
    elif numJornada == 21:
        with open("{{url_for('static', filename='./TFG WorkSpace/jornadas/jornada21.json')}}") as file:
            i = 0
            dataPersonalizado = json.load(file)    
            diccionarioDatosPersonalizado = dataPersonalizado['data']
            listaClasificacionPersonalizada = diccionarioDatosPersonalizado['table']
            while i<len(listaClasificacionPersonalizada):
                if listaClasificacionPersonalizada[i].get('name') == equipo:
                    puntos = int(listaClasificacionPersonalizada[i].get('points'))
                    break
                i += 1
    
    return puntos

equipo = 'Barcelona'
jornada = 21
print(puntuacionPersonalizada(equipo,jornada))
