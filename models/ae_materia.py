from odoo import models, fields, api

class Materia(models.Model):
    _name = 'agenda.materia'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'


    nombre = fields.Char(string="Nombre")

    creador_id = fields.Many2one('res.partner', string="Persona") 

    horario_ids = fields.One2many('agenda.materia.horario', 'materia_id', string="Horarios")  # Relación con tabla intermedia




