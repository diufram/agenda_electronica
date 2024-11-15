from odoo import http
from odoo.http import request
import json
import base64
import requests
import re

class ApiAlumnoController(http.Controller):
    # Definir una ruta para obtener todos los cursos
    @http.route('/api/alumno/materias/<int:alumno_id>', type='http', auth='public', methods=['GET'], csrf=False)
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

    @http.route('/api/alumno/<int:alumno_id>/presentar/tarea/<int:tarea_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def presentar_tarea(self, alumno_id , tarea_id, **kwargs):
        
        tarea_alumno = request.env['agenda.tarea.alumno'].sudo().search([('tarea_id', '=' , tarea_id),('alumno_id', '=' , alumno_id)])
        
        archivo = request.httprequest.files.get('archivo')
        
        # Procesar el archivo si existe
        archivo_datos = None
        archivo_nombre = None
        if archivo:
            archivo_datos = base64.b64encode(archivo.read()).decode('utf-8')  # Convertir el archivo a base64
            archivo_nombre = archivo.filename

        tarea_alumno.write({'estado': True, 'archivo_nombre':archivo_nombre , 'archivo_datos': archivo_datos,})

        # Devolver una respuesta JSON válida
        return http.Response(
            json.dumps({'status': 'success'}),
            content_type='application/json',
            status=200
        )
    

    @http.route('/api/alumno/generar-horario/<int:alumno_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def generar_horario_con_ia(self, alumno_id, **kwargs):
        alumno = request.env['agenda.alumno.curso'].sudo().search([('alumno_id','=',alumno_id)])
        curso_id = alumno.curso_id.id
        materias_horarios = request.env['agenda.materia.horario'].sudo().search([('curso_id','=',curso_id)])
        data = []

        for materia_horario in materias_horarios:
            data.append({
                'Materia': materia_horario.materia_id.nombre,
                'hora_inicio': materia_horario.horario_id.hora_inicio,
                'hora_fin':  materia_horario.horario_id.hora_fin,
            })
        disponibilidad_de_estudio = "14:00 a 18:00"
        tiempo_de_estudio = ""
        salida = '''
{
    "Lunes": [
        {"Materia": "Matematicas", "hora inicio": "14:00", "hora fin": "14:30"},
        {"Materia": "Filosofia", "hora inicio": "14:30", "hora fin": "15:00"}
    ],
    "Martes": [
        {"Materia": "Ciencias Naturales", "hora inicio": "14:00", "hora fin": "14:30"}
    ]
}
'''
        from ..utils import config
        apiKey = config.OPENAI_API_KEY
        promt = f""" 
Quiero generar un horario de estudio aparte basado en mi horario actual de clases. Aquí está mi horario de clases:

{data}

Quiero un horario de estudio complementario con las siguientes condiciones:

1. Dedicar **30 minutos** de estudio a cada materia.
2. El horario de estudio debe estar fuera del horario de clases.
3. Mi disponibilidad para estudiar es de **"14:00 a 18:00"**.
4. Las materias deben distribuirse de forma aleatoria para que no sigan siempre el mismo orden.
5. El horario generado debe ser diferente cada vez que se realice esta consulta.
6. La salida debe ser un JSON organizado por días de la semana con esta estructura exacta:

{salida}

Por favor, devuelve **solo el JSON** sin explicaciones ni texto adicional.
         """
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': f'{apiKey}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': 'gpt-4',
            'messages': [
                {'role': 'user', 'content': promt}
            ],
            'max_tokens': 5000,
            'temperature': 0.7,
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Levanta una excepción si hay un error HTTP
            data = response.json()
            respuesta = data.get('choices', [{}])[0].get('message', {}).get('content', "Sin respuesta")
            json_str = re.search(r'{.*}', respuesta, re.DOTALL).group() 
            print(json_str)
            return json_str
        
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error al llamar a la API de OpenAI: {e}")
        
    @http.route('/api/alumno/guardar-horario/<int:alumno_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def guardar_horario_generado(self, alumno_id, **kwargs):
        data = json.loads(request.httprequest.data.decode('utf-8'))
        horario = data.get('horario')
        alumno = request.env['agenda.alumno'].sudo().search([('id', '=' , alumno_id)])
        alumno.write({'horario_generado':horario})

    @http.route('/api/alumno/horario/<int:alumno_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_horario_generado(self, alumno_id, **kwargs):
        alumno = request.env['agenda.alumno'].sudo().search([('id', '=' , alumno_id)])

        return http.Response(
            json.dumps(alumno.horario_generado),
            status=200,
            mimetype='application/json'
        )
        
        
