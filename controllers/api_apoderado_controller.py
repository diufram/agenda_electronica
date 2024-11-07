
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

            curso = request.env['agenda.alumno.materia'].sudo().search([('alumno_id', '=', alumno.alumno_id.id)], limit=1)
       
            data.append({
                    'alumno_id': alumno.alumno_id.id,
                    'alumno_nombre': alumno.alumno_id.name,
                    #'curso_paralelo': curso.paralelo,
                    'curso_nombre':curso.materia_horario_id.curso_id.nombre + " "+ curso.materia_horario_id.curso_id.paralelo,
                })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    

    @http.route('/api/apoderado/materias/<int:alumno_id>', type='http', auth='public', methods=['GET'], csrf=False)
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

