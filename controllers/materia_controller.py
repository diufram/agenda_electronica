from odoo import http
from odoo.http import request
import json

class MateriaController(http.Controller):
    # Definir una ruta para obtener todos los cursos
    @http.route('/api/alumno-materia/<int:alumno_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_cursos(self, alumno_id, **kwargs):
       
        alumno_materias = request.env['agenda.alumno.materia'].sudo().search([('alumno_id', '=', alumno_id)])
        data = []

        for alumno_materia in alumno_materias:
            data.append({
                'id': alumno_materia.materia_horario_id.id, 
                'materia_nombre': alumno_materia.materia_horario_id.materia_id.nombre,
                'profesor_nombre': alumno_materia.materia_horario_id.materia_horario_ids.profesor_id.name,  
            })
        print(data)
        # Devolver los datos en formato JSON
        return http.Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
        )
