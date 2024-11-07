from odoo import http
from odoo.http import request
import json
import base64

class ApiProfesorController(http.Controller):
    # Definir una ruta para obtener todos los cursos
    @http.route('/api/profesor/cursos/<int:profesor_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_cursos(self, profesor_id, **kwargs):
        # Filtramos por el profesor_id pasado como parámetro
        profe_materia_horario = request.env['agenda.materia.horario'].sudo().search([('profesor_id', '=', profesor_id)])

        data = []
        seen_courses = set()  # Conjunto para almacenar los cursos ya añadidos

        for materia_horario in profe_materia_horario:
            curso = materia_horario.curso_id
            # Verificamos si el curso ya ha sido añadido para evitar duplicados
            if curso.id not in seen_courses:
                seen_courses.add(curso.id)
                data.append({
                    'curso_id': curso.id,
                    'curso_nombre': curso.nombre,
                    'curso_paralelo': curso.paralelo,
                })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    @http.route('/api/profesor/<int:profesor_id>/cursos/<int:curso_id>/materias', type='http', auth='public', methods=['GET'], csrf=False)
    def get_materias_from_cursos(self, curso_id,profesor_id, **kwargs):
        # Filtramos por el profesor_id pasado como parámetro
        profe_materia_horario = request.env['agenda.materia.horario'].sudo().search([('profesor_id', '=', profesor_id),('curso_id', '=', int(curso_id))])
        
        data = []
        for alumno_materia in profe_materia_horario:
            materia = alumno_materia.materia_id
            horario = alumno_materia.horario_id
            cantidad_alumnos = request.env['agenda.alumno.materia'].sudo().search_count([('materia_horario_id', '=', alumno_materia.id)])
            data.append({
                'id': alumno_materia.id, 
                'materia_nombre': materia.nombre,
                'horario':horario.hora_inicio + "-" + horario.hora_fin ,  
                'cantidad_alumnos': cantidad_alumnos,
            })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    
    @http.route('/api/profesor/tareas/<int:materia_horario_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_tareas_from_materia(self, materia_horario_id ,**kwargs):
        # Filtramos por el profesor_id pasado como parámetro
        tareas = request.env['agenda.tarea'].sudo().search([('materia_horario_id', '=', materia_horario_id)])
        
        data = []
        for tarea in tareas:

            cantidad_presentados = request.env['agenda.tarea.alumno'].sudo().search_count([('tarea_id', '=', tarea.id)])
            data.append({
                'id': tarea.id, 
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'fecha_presentacion':tarea.fecha_presentacion.isoformat(),  
                'cantidad_presentados': cantidad_presentados,
            })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    @http.route('/api/profesor/asistencia/<int:materia_horario_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_alumnos_materia_for_asistencia(self, materia_horario_id ,**kwargs):
        # Filtramos por el profesor_id pasado como parámetro
        alumnos_materia = request.env['agenda.alumno.materia'].sudo().search([('materia_horario_id', '=', materia_horario_id)])
  
        data = []
        for alumno in alumnos_materia:

            data.append({
                'id': alumno.alumno_id.id, 
                'nombre': alumno.alumno_id.name,
            })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    
    @http.route('/api/profesor/crear/tarea/<int:materia_horario_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def create_tarea(self, materia_horario_id, **kwargs):
        # Obtener los datos JSON enviados en el campo 'data'
        data = json.loads(request.httprequest.form.get('data', '{}'))
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        fecha_presentacion = data.get('fecha_presentacion')
        
        # Obtener archivo adjunto desde la solicitud
        archivo = request.httprequest.files.get('archivo')
        
        # Procesar el archivo si existe
        archivo_datos = None
        archivo_nombre = None
        if archivo:
            archivo_datos = base64.b64encode(archivo.read()).decode('utf-8')  # Convertir el archivo a base64
            archivo_nombre = archivo.filename

        # Crear el registro en el modelo 'agenda.tarea'
        tarea_creada = request.env['agenda.tarea'].sudo().create({
            'titulo': titulo,
            'descripcion': descripcion,
            'fecha_presentacion': fecha_presentacion,
            'materia_horario_id': materia_horario_id,
            'archivo_nombre': archivo_nombre,
            'archivo_datos': archivo_datos,
        })

        # Devolver una respuesta JSON válida
        return http.Response(
            json.dumps({'status': 'success', 'tarea_id': tarea_creada.id}),
            content_type='application/json',
            status=200
        )
