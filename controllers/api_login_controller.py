from odoo import http
from odoo.http import request
import json

class ApiLoginController(http.Controller):

    @http.route('/api/login', type='http', auth='public', methods=['POST'], csrf=False)
    def api_login(self, **kwargs):

        # Leer el JSON desde la solicitud HTTP
        data = json.loads(request.httprequest.data.decode('utf-8'))
        ci = data.get('ci')
        token = data.get('token')

        # Buscar en las tablas correspondientes
        es_profesor = request.env['agenda.profesor'].sudo().search([('ci', '=', ci)], limit=1)
        es_apoderado = request.env['agenda.apoderado'].sudo().search([('ci', '=', ci)], limit=1)
        es_alumno = request.env['agenda.alumno'].sudo().search([('ci', '=', ci)], limit=1)

        # Verificar si el usuario es un profesor
        if es_profesor.exists():
            es_profesor.write({'token': token})
            return http.Response(
                json.dumps({
                    'id': es_profesor.id,
                    'nombre': es_profesor.user_id.name,
                    'tipo': 1,
                }),
                status=200,
                mimetype='application/json'
            )

        # Verificar si el usuario es un apoderado
        elif es_apoderado.exists():
            es_apoderado.write({'token': token})
            return http.Response(
                json.dumps({
                    'id': es_apoderado.id,
                    'nombre': es_apoderado.user_id.name,
                    'tipo': 2,
                }),
                status=200,
                mimetype='application/json'
            )

        # Verificar si el usuario es un alumno
        elif es_alumno.exists():
            es_alumno.write({'token': token})
            return http.Response(
                json.dumps({
                    'id': es_alumno.id,
                    'nombre': es_alumno.user_id.name,
                    'tipo': 3,
                }),
                status=200,
                mimetype='application/json'
            )

        # Si no se encuentra ningún usuario
        return http.Response(
            json.dumps({
                'status': False,
                'error': 'No se encontró ningún usuario con ese CI'
            }),
            status=401,
            mimetype='application/json'
        )



