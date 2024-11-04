from odoo import models, fields, api

class Asistencia(models.Model):
    _name = 'agenda.asistencia'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    fecha = fields.Date(string="Fecha")

    materia_horario_id = fields.Many2one('agenda.materia.horario', string="Materia Horario", required=True)