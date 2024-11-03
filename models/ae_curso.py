from odoo import models, fields, api

class Curso(models.Model):
    _name = 'agenda.curso'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    nivel = fields.Char(string="Nivel")
    nombre = fields.Char(string="Nombre")
    paralelo = fields.Char(string="Paralelo")

    creador_id = fields.Many2one('res.partner', string="Persona") 

    materia_horarios_ids = fields.One2many('agenda.materia.horario', 'curso_id', string="Cursos")
