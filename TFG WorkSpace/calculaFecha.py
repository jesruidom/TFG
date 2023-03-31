from datetime import date

fecha = date.today()

def calculaFechaAnterior(fecha):
    diaActual = fecha.day
    mesActual = fecha.month
    mesPasado = mesActual-1
    anio = fecha.year

    if diaActual == 31:
        diaFin = 28
    else:
        diaFin = diaActual

    if mesPasado == 0:
        mesPasado = 12
        anio = fecha.year -1

    fechaAnterior = fecha.replace(day=diaFin)
    fechaAnterior = fechaAnterior.replace(month=mesPasado)
    fechaAnterior = fechaAnterior.replace(year=anio)

        
    return fechaAnterior

print(calculaFechaAnterior(fecha))