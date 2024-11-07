from odoo import http
from odoo.http import request
import json

class ApiAlumnoController(http.Controller):
    # Definir una ruta para obtener todos los cursos
    @http.route('/api/alumno/materias/<int:alumno_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def getMateriasFromAlumno(self, alumno_id, **kwargs):
       
        alumno_materias = request.env['agenda.alumno.materia'].sudo().search([('alumno_id', '=', alumno_id)])
        data = []

        for alumno_materia in alumno_materias:
            data.append({
                'id': alumno_materia.materia_horario_id.id, 
                'materia_nombre': alumno_materia.materia_horario_id.materia_id.nombre,
                'profesor_nombre': alumno_materia.materia_horario_id.profesor_id.name,  
            })
     
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )

    @http.route('/api/alumno/tareas/<int:materia_horario_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_tareas_from_materia(self, materia_horario_id, **kwargs):
       
        tareas = request.env['agenda.tarea'].sudo().search([('materia_horario_id', '=', materia_horario_id)])
        
        data = []
        for tarea in tareas:


            data.append({
                'id': tarea.id, 
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'fecha_presentacion':tarea.fecha_presentacion.isoformat(),  
                'archivo_nombre':tarea.archivo_nombre,  
            })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    
    @http.route('/api/alumno/tarea/<int:tarea_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_tarea(self, tarea_id, **kwargs):
        # Obtener el registro de la tarea por su ID
        tarea = request.env['agenda.tarea'].sudo().search([('id', '=', tarea_id)], limit=1)
        

        # Convertir el archivo adjunto a formato base64 si existe
        archivo_datos = tarea.archivo_datos.decode('utf-8') if tarea.archivo_datos else None

        # Preparar los datos para la respuesta
        tarea_data = {
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'fecha_presentacion': tarea.fecha_presentacion.strftime('%Y-%m-%d') if tarea.fecha_presentacion else None,
            'materia_horario_id': tarea.materia_horario_id.id if tarea.materia_horario_id else None,
            'archivo_nombre': tarea.archivo_nombre,
            'archivo_datos': archivo_datos,  # Archivo en base64 para ser mostrado en la respuesta
        }

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps({'status': 'success', 'tarea': tarea_data}),
            content_type='application/json',
            status=200
        )
