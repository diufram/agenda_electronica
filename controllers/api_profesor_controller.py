from odoo import http
from odoo.http import request
import json
import base64
import requests

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
        cantidad_alumnos = request.env['agenda.alumno.curso'].sudo().search_count([('curso_id', '=', curso_id)])
        for alumno_materia in profe_materia_horario:
            materia = alumno_materia.materia_id
            horario = alumno_materia.horario_id
            
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

            cantidad_presentados = request.env['agenda.tarea.alumno'].sudo().search_count([('tarea_id', '=', tarea.id ),('estado', '=', True )])
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
        materia_horario = request.env['agenda.materia.horario'].sudo().search([('id', '=', materia_horario_id)])
        curso_id= materia_horario.curso_id.id
        alumnos_materia = request.env['agenda.alumno.curso'].sudo().search([('curso_id', '=', curso_id)])
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

        materia_horario = request.env['agenda.materia.horario'].sudo().search([('id', '=', materia_horario_id)])
        curso_id= materia_horario.curso_id.id
        alumnos_materia = request.env['agenda.alumno.curso'].sudo().search([('curso_id', '=', curso_id)])

        apoderados_enviar = []
        alumnos_enviar = []

        for alumno in  alumnos_materia:
            if alumno.alumno_id.token:
                alumnos_enviar.append(alumno.alumno_id.token)
            if alumno.alumno_id.apoderado_ids.apoderado_id.token: 
                apoderados_enviar.append(alumno.alumno_id.apoderado_ids.apoderado_id.token)

        #PARA APODERADOS
        self._send_notification(personas=apoderados_enviar, titulo= "Se le asigno una tarea a su Hijo, Titulo: "+ titulo, descripcion= "Descripcion: "+descripcion)

        #PARA ALUMNOS
        self._send_notification(personas=alumnos_enviar, titulo= "Se le asigno una tarea, Titulo: "+ titulo, descripcion= "Descripcion: "+descripcion)

        for alumno in  alumnos_materia:
            request.env['agenda.tarea.alumno'].sudo().create({
            'tarea_id': tarea_creada.id,
            'alumno_id': alumno.alumno_id.id,
            })
            

        # Devolver una respuesta JSON válida
        return http.Response(
            json.dumps({'status': 'success', 'tarea_id': tarea_creada.id}),
            content_type='application/json',
            status=200
        )

    @http.route('/api/profesor/tomar/asistencia/<int:materia_horario_id>',type='http', auth='public', methods=['POST'], csrf=False)
    def tomar_asistencia(self, materia_horario_id, **kwargs):
        data = json.loads(request.httprequest.data.decode('utf-8'))
        alumnos_id = data.get('alumnos_id')

        materia_horario = request.env['agenda.materia.horario'].sudo().search([('id', '=', materia_horario_id)])
        curso_id= materia_horario.curso_id.id
        alumnos_materia = request.env['agenda.alumno.curso'].sudo().search([('curso_id', '=', curso_id)])
        asistencia = request.env['agenda.asistencia'].sudo().create({
            'materia_horario_id': materia_horario_id,
        })

        for alumno in  alumnos_materia:
            request.env['agenda.asistencia.alumno'].sudo().create({
            'estado': alumno.alumno_id.id in  alumnos_id,
            'alumno_id': alumno.alumno_id.id,
            'asistencia_id': asistencia.id
        })
        return http.Response(
            json.dumps({'status': 'success', 'asistencia': asistencia.id}),
            content_type='application/json',
            status=200
        )
        



    def _send_notification(self, personas, titulo, descripcion):

        url = "https://api.onesignal.com/notifications"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic YTgzNWVlYzMtYmQ2ZS00ZjA1LWFmNzMtNTUyMmNmMzE5MTY5'  # Tu clave de API
        }
        payload = {
            "target_channel": "push",
            "included_segments": ["Subscribed Users"],
            "app_id": "bde019e1-c5b5-4852-9135-a829a99244b1",  # Tu ID de aplicación de OneSignal
            "contents": {"en": descripcion},
            "include_subscription_ids": personas,
            "headings": {"en": titulo}
        }

        # Realiza la solicitud POST a OneSignal
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Verifica si hay errores HTTP

            # Construye una respuesta válida para Odoo
            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'message': 'Notificación enviada exitosamente',
                    'response': response.json()
                }),
                headers={'Content-Type': 'application/json'}
            )
        except requests.exceptions.RequestException as e:
            # Manejo de errores con una respuesta válida
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': 'Error al enviar la notificación',
                    'details': str(e)
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
 
    @http.route('/api/profesor/asistencias/<int:materia_horario_id>',type='http', auth='public', methods=['GET'], csrf=False)
    def get_asistencias_from_materia(self, materia_horario_id, **kwargs):
        data = []

        asistencias = request.env['agenda.asistencia'].sudo().search([('materia_horario_id', '=', materia_horario_id)])
        
        for asistencia in asistencias:
            cantidad_presentes = request.env['agenda.asistencia.alumno'].sudo().search_count([('asistencia_id', '=', asistencia.id),('estado', '=', True)])
            data.append({
                'asistencia_id': asistencia.id,
                'fecha': asistencia.fecha.isoformat(), 
                'cant_alumnos_presentes': cantidad_presentes

            })

        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    
    @http.route('/api/profesor/tareas-presentadas/<int:tarea_id>',type='http', auth='public', methods=['GET'], csrf=False)
    def get_tareas_presentadas_tarea(self, tarea_id, **kwargs):
        tareas = request.env['agenda.tarea.alumno'].sudo().search([('tarea_id', '=', tarea_id),('estado','=',True)])
        data = []
        for tarea in tareas:
            data.append({
                'tarea_alumno_id': tarea.id,
                'alumno_nombre': tarea.alumno_id.name,
                'archivo_nombre':tarea.archivo_nombre,  
                'nota': tarea.nota
            })

        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    

    @http.route('/api/profesor/tarea-alumno/<int:tarea_alumno_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_tarea(self, tarea_alumno_id, **kwargs):
        # Obtener el registro de la tarea por su ID
        tarea = request.env['agenda.tarea.alumno'].sudo().search([('id', '=', tarea_alumno_id)], limit=1)
        

        # Convertir el archivo adjunto a formato base64 si existe
        archivo_datos = tarea.archivo_datos.decode('utf-8') if tarea.archivo_datos else None

        # Preparar los datos para la respuesta
        tarea_data = {

            'archivo_nombre': tarea.archivo_nombre,
            'archivo_datos': archivo_datos,  # Archivo en base64 para ser mostrado en la respuesta
        }

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps({'status': 'success', 'tarea': tarea_data}),
            content_type='application/json',
            status=200
        )

    @http.route('/api/profesor/asignar/<int:tarea_alumno_id>/nota',type='http', auth='public', methods=['POST'], csrf=False)
    def asignar_nota(self, tarea_alumno_id, **kwargs):
        tarea_alumno = request.env['agenda.tarea.alumno'].sudo().browse(tarea_alumno_id)
        print(tarea_alumno.nota)
        data = json.loads(request.httprequest.data.decode('utf-8'))
        nota = data.get('nota')
        tarea_alumno.write({'nota': nota})
        return http.Response(   
            json.dumps({'status': 'success'}),
            content_type='application/json',
            status=200
        )