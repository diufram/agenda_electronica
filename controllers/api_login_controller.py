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

            user = request.env['res.users'].sudo().search([('ci', '=', ci)])


            if user:
                tipo = 1
                if user.es_profesor:
                    tipo = 1
                elif user.es_apoderado:
                    tipo = 2
                elif user.es_alumno:
                     tipo = 3
                user.write({'token': token})
                return http.Response(
                json.dumps({
                'id': user.id, 
                'nombre': user.name,
                'tipo': tipo,
                }),
                status=200,
                mimetype='application/json'
                )
            else: 
                return http.Response(
                json.dumps({
                'status': False,
                'error': 'No se encontro ningun usuario con ese CI'
                }),
                status=401,
                mimetype='application/json'
                )

            
