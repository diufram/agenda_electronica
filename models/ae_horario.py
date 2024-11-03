from odoo import models, fields, api

class Horario(models.Model):
    _name = 'agenda.horario'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'


    hora_inicio = fields.Char(string="Hora de Inicio")
    hora_fin = fields.Char(string="Hora de Fin")

    materia_ids = fields.One2many('agenda.materia.horario', 'horario_id', string="Materias")





