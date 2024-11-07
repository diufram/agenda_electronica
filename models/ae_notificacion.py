from odoo import models, fields, api

class Notificacion(models.Model):
    _name = 'agenda.notificacion'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'


    titulo = fields.Char(string="Titulo")
    mensaje = fields.Text(string="Mensaje")

    creador_id = fields.Many2one('res.users', string="Persona") 




