from odoo import models, fields, api

class MateriaHorario(models.Model):
    _name = 'agenda.materia.horario'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    materia_id = fields.Many2one('agenda.materia', string="Materia", required=True)
    horario_id = fields.Many2one('agenda.horario', string="Horario", required=True)
    curso_id = fields.Many2one('agenda.curso', string="Curso", required=True) 

    alumnos_ids = fields.One2many('agenda.alumno.materia', 'materia_horario_id', string="Alumnos")




