from odoo import models, fields, api

class ProfeMateria(models.Model):
    _name = 'agenda.profe.materia'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    materia_horario_id = fields.Many2one('agenda.materia.horario', string="Materia Horario", required=True)

    profesor_id = fields.Many2one('res.partner', string="Profesor", required=True) 

    asistencia_ids = fields.One2many('agenda.asistencia', 'materia_id', string="Asistencias de La Materia")

    tarea_ids = fields.One2many('agenda.tarea', 'profe_materia_id', string="Tareas de la Materia")
    
    
