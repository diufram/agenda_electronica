from odoo import models, fields

class ApoderadoAlumno(models.Model):
    _name = 'agenda.apoderado.alumno'
    _description = 'Relación entre Apoderado y Alumno'

    apoderado_id = fields.Many2one('agenda.apoderado', string="Apoderado", required=True)
    alumno_id = fields.Many2one('agenda.alumno', string="Alumno", required=True)
