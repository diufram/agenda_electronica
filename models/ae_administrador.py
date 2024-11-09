from odoo import models, fields

class Administrador(models.Model):
    _name = 'agenda.administrador'
    _inherits = {'res.users': 'user_id'}
    _description = 'Modelo para personas en la agenda'

    user_id = fields.Many2one('res.users', required=True, ondelete="cascade")



