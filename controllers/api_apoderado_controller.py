
from odoo import http
from odoo.http import request
import json

class ApiApoderadoController(http.Controller):
    # Definir una ruta para obtener todos los cursos
    @http.route('/api/apoderado/<int:apoderado_id>/hijos', type='http', auth='public', methods=['GET'], csrf=False)
    def get_alumnos_from_apoderado(self, apoderado_id, **kwargs):
        # Filtramos por el profesor_id pasado como parámetro
        alumnos_from_apoderado = request.env['agenda.apoderado.alumno'].sudo().search([('apoderado_id', '=', apoderado_id)])
        data = []
        seen_courses = set()  # Conjunto para almacenar los cursos ya añadidos

        for alumno in alumnos_from_apoderado:
            #curso = materia_horario.curso_id
            # Verificamos si el curso ya ha sido añadido para evitar duplicados
            
            data.append({
                    'alumno_id': alumno.alumno_id.id,
                    'alumno_nombre': alumno.alumno_id.name,
                    #'curso_paralelo': curso.paralelo,
                })

        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )

