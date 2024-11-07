from odoo import models, fields, api

class AlumnoMateria(models.Model):
    _name = 'agenda.alumno.materia'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    materia_horario_id = fields.Many2one('agenda.materia.horario', string="Materia", required=True)
    alumno_id = fields.Many2one('res.users', string="Alumno", required=True)





