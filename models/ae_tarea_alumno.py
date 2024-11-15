from odoo import models, fields, api

class TareaAlumno(models.Model):
    _name = 'agenda.tarea.alumno'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    estado = fields.Boolean(string="Presentado", default=False)
    visto = fields.Boolean(string="Fue Visto", default=False) # PARA VERIFICAR SI EL PADRE LO VIO 
    archivo_nombre = fields.Char(string="Nombre del Archivo")
    archivo_datos = fields.Binary(string="Archivo Adjunto", attachment=True)
    nota = fields.Float(string="Nota", default= 0.0)

    tarea_id = fields.Many2one('agenda.tarea', string="Tarea", required=True)
    alumno_id = fields.Many2one('agenda.alumno', string="Alumno", required=True) 



