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

    fechaAnterior = fecha.replace(month=mesPasado)
    fechaAnterior = fechaAnterior.replace(year=anio)
    return fechaAnterior

#Obtenemos el mes anteior para sustituirlo en la llamada a la API y pedir los resultados a partir de un mes anteior


print(f'La fecha de hoy es {fecha}')
print(f'La fecha de hace un mes es {calculaFechaAnterior(fecha)}')


print('Hello world')

l = [1, 4, 5, 6, 8, 3, 5, 8]

for i in l:
    print("El elemento iesimo es:", i)


nombre = "Jose"
print(f"mi nombre es {nombre}")

    
