from odoo import models, fields, api

class AsistenciaAlumno(models.Model):
    _name = 'agenda.asistencia.alumno'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    estado = fields.Boolean(string= "Estado")

    asistencia_id = fields.Many2one('agenda.asistencia', string="Asistencia", required=True)
    alumno_id = fields.Many2one('agenda.alumno', string="Alumno", required=True)