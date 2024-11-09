from odoo import models, fields, api

class AlumnoCurso(models.Model):
    _name = 'agenda.alumno.curso'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    curso_id = fields.Many2one('agenda.curso', string="Curso", required=True)
    alumno_id = fields.Many2one('agenda.alumno', string="Alumno", required=True)





