from odoo import models, fields

class ApoderadoAlumno(models.Model):
    _name = 'agenda.apoderado.alumno'
    _description = 'Relación entre Apoderado y Alumno'

    apoderado_id = fields.Many2one('res.users', string="Apoderado", required=True)
    alumno_id = fields.Many2one('res.users', string="Alumno", required=True)
