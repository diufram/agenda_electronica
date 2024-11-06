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
            })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )