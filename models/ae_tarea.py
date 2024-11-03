from odoo import models, fields, api

class Tarea(models.Model):
    _name = 'agenda.tarea'  # Nombre único del modelo
    _description = 'Modelo para personas en la agenda'

    descripcion = fields.Text(string="Descripcion")
    #archivos = fil
    titulo = fields.Char(string="Titulo", help="Titulo de la Tarea")
    fecha_presentacion = fields.Date(string="Fecha de Presentacion")
    profe_materia_id = fields.Many2one('agenda.profe.materia', string="Profe Materia", required=True)
    alumno_ids = fields.One2many('agenda.tarea.alumno', 'tarea_id', string="Alumno")

    
 


