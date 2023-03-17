from django.shortcuts import redirect, render
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User, auth
import calendar


from .models import Objetivo
from django.contrib.auth.decorators import login_required
# Create your views here.
FECHA_ACTUAL = date.today()

@login_required
def index(request):
    # obtenemos la fecha actual
    fecha_actual = datetime.now()

    # obtenemos el año y el mes actual
    anio = fecha_actual.year
    mes = fecha_actual.month

    # creamos un diccionario de 2 meses
    meses = {}

    # llenamos el diccionario con las semanas de los 2 meses
    for i in range(2):
        semanas = obtenerSemanas(mes+i, anio)
        meses[i] = semanas


    # contexto
    context = {
        'meses': meses,
    }
    
    return render(request, 'index.html', context)

# funcion para obtener una lista de semanas con los dias de un mes especifico
def obtenerSemanas(mes, anio):
    # recibe el mes y el año
    # Obtener el número de días del mes y el primer día de la semana
    primer_dia, num_dias = calendar.monthrange(anio, mes)

    # Obtener el nombre del mes
    nombre_mes = calendar.month_name[mes]
 
    # Crear una lista de semanas vacías
    semanas = []

    # Llena de nulos los primeros días que no pertenecen al mes
    semana = [None] * primer_dia

    # Llena la lista de semanas con los días del mes
    for dia in range(1, num_dias + 1):
        semana.append(dia)

        # Si la semana está llena, agregarla a la lista de semanas y crear una nueva
        if len(semana) == 7:
            semanas.append(semana)
            semana = []

    # Si la semana no está vacía, agregarla a la lista de semanas
    if semana:
        # Llena la semana de fin de mes con nulos hasta completar los 7 días
        semana += [None] * (7 - len(semana))
        semanas.append(semana)

    # retorna la lista de semanas, el mes, el nombre del mes en ingles y el año
    return {
        'semanas': semanas,
        'mes': mes,
        'nombre_mes': nombre_mes,
        'anio': anio,
    }

# etiqueta para el login obligatorio
@login_required
def actividad(request):
    try:
        # obtenemos el dia, numero de mes, nombre del mes, año y el objetivo del formulario
        dia = int(request.POST['dia'])
        mes = int(request.POST['mes'])
        anio = int(request.POST['anio'])
        mesnom = request.POST['mesnom']

        descripcion = request.POST['objetivo']

        # creamos la fecha con los datos del formulario
        fecha = date(anio, mes, dia)

        # obtenemos el primer dia de la semana y el ultimo dia de la semana
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

        # creamos el objetivo
        objetivo = Objetivo(descripcion=descripcion, fecha_inicio=inicio_semana, fecha_fin=fin_semana, user=request.user)
        # guardamos el objetivo
        objetivo.save()

    except Exception as e:
        print(e) 
    
    return redirect('/')


@login_required
def objetivos(request):
    # obtenemos los objetivos del usuario
    objetivos = Objetivo.objects.filter(user=request.user).order_by('fecha_inicio')

    # creamos un diccionario con las fechas de los objetivos
    objetivos_fecha = {}
    # recorremos los objetivos del usuario
    for objetivo in objetivos:

        # obtenemos la fecha de inicio y la fecha de fin
        fecha_ini = objetivo.fecha_inicio
        fecha_fin = objetivo.fecha_fin

        # creamos una clave con la fecha de inicio y la fecha de fin para agrupar los objetivos por fechas
        clave = fecha_ini.strftime('%d/%m/%Y') + ' - ' + fecha_fin.strftime('%d/%m/%Y')

        # creamos una variable editar para saber si el objetivo se puede editar o no
        # se puede editar si la fecha actual esta entre la fecha de inicio y la fecha de fin
        editar = True if FECHA_ACTUAL >= fecha_ini and FECHA_ACTUAL <= fecha_fin else False

        # creamos un diccionario con los datos del objetivo
        nuevo_objetivo = {
            'id': objetivo.id,
            'descripcion': objetivo.descripcion,
            'fecha_inicio': objetivo.fecha_inicio,
            'fecha_fin': objetivo.fecha_fin,
            # creamos una lista con el numero de veces que se ha cumplido el objetivo como si fueran dias
            'contador': [1]*objetivo.contador + [0]*(7-objetivo.contador),
            'cumplidos': objetivo.contador,
        }

        # si la clave no existe en el diccionario de objetivos por fecha, la creamos
        if clave not in objetivos_fecha: 
            # creamos una lista con el objetivo y la variable editar
            objetivos_fecha[clave] = [[], editar] 
        # agregamos el objetivo a la lista
        objetivos_fecha[clave][0].append(nuevo_objetivo)

    # contexto
    context = {
        'objetivos': objetivos_fecha,
    }
    return render(request, 'objetivos.html', context)

@login_required
def cumplir(request, id):
    try: 
        user = request.user
        # obtenemos el objetivo por el id
        objetivo = Objetivo.objects.get(id=id)
        # aumentamos el contador
        objetivo.contador += 1
        # guardamos el objetivo
        objetivo.save()
    except Exception as e:
        print(e)
    return redirect('/objetivos/') 

@login_required
def logout(request):
    # cerramos la sesion
    print('logout')
    auth.logout(request)
    return redirect('/')

def registrar(request):
    # si el usuario esta logueado lo redirigimos al registro
    return render(request, 'registration/registrar.html')


def registro(request):
    try:
        # obtenemos los datos del formulario
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # creamos el usuario
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        # guardamos el usuario
        user.save()
        # iniciamos sesion
        auth.login(request, user)
        # redirigimos al usuario a la pagina principal
        print('usuario creado')
        return redirect('/')
    except Exception as e:
        print(e)
    return redirect('/')

@login_required
def reporte(request):
    objetivos = Objetivo.objects.filter(user=request.user).order_by('fecha_inicio')

    # creamos un diccionario con las fechas de los objetivos
    objetivos_fecha = {}
    # recorremos los objetivos del usuario
    for objetivo in objetivos:

        # obtenemos la fecha de inicio y la fecha de fin
        fecha_ini = objetivo.fecha_inicio
        fecha_fin = objetivo.fecha_fin

        # creamos una clave con la fecha de inicio y la fecha de fin para agrupar los objetivos por fechas
        clave = fecha_ini.strftime('%d/%m/%Y') + ' - ' + fecha_fin.strftime('%d/%m/%Y')

        # creamos un diccionario con los datos del objetivo
        nuevo_objetivo = {
            'id': objetivo.id,
            'descripcion': objetivo.descripcion,
            'fecha_inicio': objetivo.fecha_inicio,
            'fecha_fin': objetivo.fecha_fin,
            # creamos una lista con el numero de veces que se ha cumplido el objetivo como si fueran dias
            'contador': [1]*objetivo.contador + [0]*(7-objetivo.contador),
            'cumplidos': objetivo.contador,
        }

        # si la clave no existe en el diccionario de objetivos por fecha, la creamos
        if clave not in objetivos_fecha: 
            # creamos una lista con el objetivo y la variable editar
            objetivos_fecha[clave] = [[], {'cumplidos': 0, 'no_cumplidos': 0, 'total': 0}]
        # agregamos el objetivo a la lista
        objetivos_fecha[clave][0].append(nuevo_objetivo)
    
    # contamos que obtetivos se han cumplido
    for fecha in objetivos_fecha:
        for objetivo in objetivos_fecha[fecha][0]:
            if objetivo['cumplidos'] == 7:
                objetivos_fecha[fecha][1]['cumplidos'] += 1
            else:
                objetivos_fecha[fecha][1]['no_cumplidos'] += 1
            objetivos_fecha[fecha][1]['total'] += 1
            
        

    # contexto
    context = {
        'objetivos': objetivos_fecha,
    }

    return render(request, 'reporte.html', context)


@login_required
def integrantes(request):
    context = {
        'integrantes': [
            'Veronica Vera',
            'Camila Yela',
            'Nelson Bolaños',
            'Juan Jojoa'
        ]
    }
    return render(request, 'integrantes.html', context)


@login_required
def eliminar(request, id):
    try: 
        user = request.user
        # obtenemos el objetivo por el id
        objetivo = Objetivo.objects.get(id=id)
        # aumentamos el contador
        objetivo.delete()
    except Exception as e:
        print(e)
    return redirect('/objetivos/') 