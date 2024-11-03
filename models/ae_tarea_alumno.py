from odoo import models, fields, api

class TareaAlumno(models.Model):
    _name = 'agenda.tarea.alumno'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    estado = fields.Boolean(string="Presentado", default=False)

    tarea_id = fields.Many2one('agenda.tarea', string="Tarea", required=True)
    alumno_id = fields.Many2one('res.partner', string="Alumno", required=True) 


