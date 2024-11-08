from odoo import models, fields, api

class AsistenciaAlumno(models.Model):
    _name = 'agenda.asistencia.alumno'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    asistencia_id = fields.Many2one('agenta.asistencia', string="Asistencia", required=True)
    alumno_id = fields.Many2one('res.users', string="Alumno", required=True)