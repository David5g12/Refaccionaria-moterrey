from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db import connection
import weasyprint
import os
os.environ["G_MESSAGES_DEBUG"] = "none"



def obtener_datos(opcion):
    titulo = ''
    columnas = []
    filas =[]

    match opcion:
        case 'tabla_1':
            titulo = 'Reporte de promedio salarial por departamento'
            columnas = ['Id departamento', 'Nombre departamento', 'Salario promedio']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id_departamento, d.nombre_departamento,
		            ROUND(AVG(e.salario), 2) as Salario_promedio
                    FROM empleados e
                    JOIN departamentos d
		            ON e.id_departamento = d.id_departamento
                    GROUP BY d.id_departamento,
                    d.nombre_departamento
                    ORDER BY d.id_departamento
                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_2':
            titulo = 'Reporte de antiguedad de empleados del departamento 20'
            columnas = ['Titulo', 'Nombre completo', 'Fecha contratacion', 'Id departamento', 'Nombre departamento', 'Antiguedad en semanas']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 'Reporte de Antiguedad' as titulo,
                        CONCAT(e.nombre,' ',e.apaterno,' ',e.amaterno) as Nombre_completo,
                        e.fecha_contratacion,
                        d.id_departamento,
                        d.nombre_departamento,
                        FLOOR((CURRENT_DATE - e.fecha_contratacion) /7) as Antiguedad_semanas
                    FROM empleados e
                    JOIN departamentos d
                        ON e.id_departamento = d.id_departamento
                    WHERE d.id_departamento = 20
                    ORDER BY Antiguedad_semanas DESC, e.apaterno ASC, e.amaterno ASC;
                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_3':
            titulo = 'Reporte de gasto total de salarios por departamento que ganan > 15000'
            columnas = ['Id departamento', 'Nombre departamento', 'Gasto total de salarios']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id_departamento, d.nombre_departamento,
                        SUM(e.salario) AS gasto_total_salarios
                    FROM empleados e
                    JOIN departamentos d
                        ON e.id_departamento = d.id_departamento
                    GROUP BY d.id_departamento,
                            d.nombre_departamento
                    HAVING SUM(e.salario) > 15000
                    ORDER BY d.id_departamento;

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_4':
            titulo = 'Reporte de gasto salarial por puesto (sin TRAN y > 2000)'
            columnas = ['Id puesto', 'Nombre_puesto', 'Gasto total de sueldos']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id_puesto, p.nombre_puesto,
                        SUM(e.salario) as gasto_total_sueldos
                    FROM empleados e
                    JOIN puestos p
                        ON e.id_puesto = p.id_puesto
                    WHERE p.id_puesto NOT LIKE '%TRAN'
                    GROUP BY p.id_puesto,
                            p.nombre_puesto
                    HAVING SUM(e.salario) > 2000
                    ORDER BY p.id_puesto;

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_5':
            titulo = 'Reporte de empleados y jefes directos'
            columnas = ['Puesto empleado', 'Nombre completo', 'Jefe directo']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.nombre_puesto AS puesto_empleado,
                        CONCAT(e.nombre,' ',e.apaterno,' ',e.amaterno) as nombre_completo,
                        CONCAT(j.nombre,' ',j.apaterno,' ',j.amaterno) AS jefe_directo
                    FROM empleados e
                    JOIN puestos p
                        ON e.id_puesto = p.id_puesto
                    LEFT JOIN empleados j
                        ON e.id_gerente = j.id_empleado
                    ORDER BY j.nombre ASC,j.apaterno ASC,j.amaterno ASC,
                            e.nombre ASC,e.apaterno ASC,e.amaterno ASC;

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_6':
            titulo = 'Reporte de equipo por jefes (ordenado por tamaño de equipo)'
            columnas = ['Nombre completo del jefe', 'Total empleados']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT CONCAT(j.nombre,' ',j.apaterno,' ',j.amaterno) AS jefe,
                        COUNT(e.id_empleado) AS total_empleados
                    FROM empleados j
                    LEFT JOIN empleados e
                        ON e.id_gerente = j.id_empleado
                    GROUP BY j.id_empleado,j.nombre,j.apaterno,j.amaterno
                    ORDER BY total_empleados DESC

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_7':
            titulo = 'Reporte geografico de empleados'
            columnas = ['Id empleado', 'Nombre completo', 'Departamento', 'Ciudad', 'Estado']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.id_empleado, 
                        CONCAT(e.nombre,' ',e.apaterno,' ',e.amaterno) as nombre_completo,
                        d.nombre_departamento,
                        c.nombre_ciudad,
                        es.nombre_estado
                    FROM empleados e
                    JOIN departamentos d
                        ON e.id_departamento = d.id_departamento
                    JOIN sucursales s
                        ON e.id_sucursal = s.id_sucursal
                    JOIN ciudades c
                        ON s.id_ciudad = c.id_ciudad
                    JOIN estados es
                        ON c.id_estado = es.id_estado
                    ORDER BY 
                        es.nombre_estado ASC,
                        c.nombre_ciudad ASC,
                        nombre_completo ASC;

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_8':
            titulo = 'Reporte por ficha de empleado'
            columnas = ['Nombre completo', 'Puesto', 'Departamento', 'Ciudad', 'Estado']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT CONCAT(e.nombre,' ',e.apaterno,' ',e.amaterno) as nombre_completo,
                        p.nombre_puesto,
                        d.nombre_departamento,
                        c.nombre_ciudad,
                        es.nombre_estado
                    FROM empleados e
                    JOIN puestos p
                        ON e.id_puesto = p.id_puesto
                    JOIN departamentos d
                        ON e.id_departamento = d.id_departamento
                    JOIN sucursales s
                        ON e.id_sucursal = s.id_sucursal
                    JOIN ciudades c
                        ON s.id_ciudad = c.id_ciudad
                    JOIN estados es
                        ON c.id_estado = es.id_estado
                    WHERE e.nombre ='PEDRO' AND e.apaterno ='ALBORES';

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_9':
            titulo = 'Reporte de empleados con salarios inferiores a IT_PROG'
            columnas = ['Id empleado', 'Nombre completo', 'Salario']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.id_empleado,
                        CONCAT(e.nombre,' ',e.apaterno,' ',e.amaterno) as nombre_completo,
                        e.salario
                    FROM empleados e
                    WHERE e.salario < (
                    SELECT MIN(em.salario)
                    FROM empleados em
                    JOIN puestos p
                        ON em.id_puesto = p.id_puesto
                    WHERE p.id_puesto = 'IT_PROG'
                    )
                    ORDER BY e.salario DESC;

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
        case 'tabla_10':
            titulo = 'Reporte de empleados sin personal a cargo'
            columnas = ['Nombre completo', 'Puesto', 'Jefe']
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        CONCAT(e.nombre,' ',e.apaterno,' ',e.amaterno) AS nombre_completo,
                        p.nombre_puesto,
                        CONCAT(j.nombre,' ',j.apaterno,' ',j.amaterno) AS jefe
                    FROM empleados e
                    LEFT JOIN empleados j
                        ON e.id_gerente = j.id_empleado
                    JOIN puestos p
                        ON e.id_puesto = p.id_puesto
                    WHERE e.id_empleado NOT IN (
                        SELECT DISTINCT id_gerente
                        FROM empleados 
                        WHERE id_gerente IS NOT NULL
                    )
                    ORDER BY p.nombre_puesto;

                """)
                consulta = cursor.fetchall() 
                filas = [list(fila) for fila in consulta]
                
    return titulo, columnas, filas

# Create your views here.

def index(request):
    opcion = request.GET.get('opcion', '')
    titulo, columnas, filas = obtener_datos(opcion)            
    return render(request, 'nominas/index.html', {'opcion': opcion, 'filas': filas, 'columnas': columnas, 'titulo': titulo})


def tablas_pdf(request):
    opcion = request.GET.get('opcion', '')
    titulo, columnas, filas = obtener_datos(opcion)
    img_url = request.build_absolute_uri('/static/img/logo.jpg') 
    html = render_to_string('nominas/pdf.html', {'titulo': titulo, 'columnas': columnas, 'filas': filas, 'img_url': img_url})
    pdf = weasyprint.HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()
    return HttpResponse(pdf, content_type='application/pdf')
    
