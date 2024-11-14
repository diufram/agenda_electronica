
from odoo import http
from odoo.http import request
import json

class ApiApoderadoController(http.Controller):
    # Definir una ruta para obtener todos los cursos
    @http.route('/api/apoderado/<int:apoderado_id>/alumnos', type='http', auth='public', methods=['GET'], csrf=False)
    def get_alumnos_from_apoderado(self, apoderado_id, **kwargs):
        # Filtramos por el profesor_id pasado como parámetro
        alumnos_from_apoderado = request.env['agenda.apoderado.alumno'].sudo().search([('apoderado_id', '=', apoderado_id)])
        data = []

        for alumno in alumnos_from_apoderado:

            curso = request.env['agenda.alumno.curso'].sudo().search([('alumno_id', '=', alumno.alumno_id.id)], limit=1)
            if curso:
                data.append({
                    'alumno_id': alumno.alumno_id.id,
                    'alumno_nombre': alumno.alumno_id.name,
                    #'curso_paralelo': curso.paralelo,
                    'curso_nombre':curso.curso_id.nombre + " " + curso.curso_id.paralelo,
                })
            
        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    

    @http.route('/api/apoderado/materias/<int:alumno_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def getMateriasFromAlumno(self, alumno_id, **kwargs):
       
        alumno_curso = request.env['agenda.alumno.curso'].sudo().search([('alumno_id', '=', alumno_id)])
        alumno_materias = alumno_curso.curso_id.materia_horarios_ids
        data = []

        for alumno_materia in alumno_materias:
            data.append({
                'id': alumno_materia.id, 
                'materia_nombre': alumno_materia.materia_id.nombre,
                'profesor_nombre': alumno_materia.profesor_id.name,  
            })
     
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    
    @http.route('/api/apoderado/notificaciones/<int:apoderado_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_notificaciones(self, apoderado_id, **kwargs):
        alumnos_from_apoderado = request.env['agenda.apoderado.alumno'].sudo().search([('apoderado_id', '=', apoderado_id)])
        data = []
        for alumno in alumnos_from_apoderado:
            tareas = request.env['agenda.tarea.alumno'].sudo().search([('alumno_id', '=', alumno.alumno_id.id),('estado', '=', False),('visto', '=', False)])
            for tarea in tareas:
                materia = tarea.tarea_id.materia_horario_id.materia_id.nombre
                data.append({
                'tarea_id': tarea.id,
                'titulo': tarea.tarea_id.titulo,
                'descripcion': tarea.tarea_id.descripcion,
                'alumno_nombre': alumno.alumno_id.name,
                'materia_nombre': materia,
                'profesor_nombre': tarea.tarea_id.materia_horario_id.profesor_id.name,
                'fecha_presentacion':tarea.tarea_id.fecha_presentacion.isoformat()
                })
        
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    

    @http.route('/api/apoderado/notificaciones/marcar/<int:idTareaAlumno>', type='http', auth='public', methods=['GET'], csrf=False)
    def marcarTarea(self, idTareaAlumno, **kwargs):
        tarea_alumno = request.env['agenda.tarea.alumno'].sudo().browse(idTareaAlumno)
        tarea_alumno.write({'visto': True})
        

    @http.route('/api/apoderado/tareas/<int:idAlumno>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_tareas_from_alumno(self, idAlumno, **kwargs):
        tareas_alumno = request.env['agenda.tarea.alumno'].sudo().search([('alumno_id', '=', idAlumno)])
        data = []
        for tarea in tareas_alumno:
            data.append({
                'tarea_id': tarea.tarea_id.id,
                'titulo': tarea.tarea_id.titulo,
                'descripcion': tarea.tarea_id.descripcion,
                'profesor_nombre': tarea.tarea_id.materia_horario_id.profesor_id.name,
                'fecha_presentacion':tarea.tarea_id.fecha_presentacion.isoformat(),
                'estado': tarea.estado
                })

        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        
