from odoo import models, fields

class Persona(models.Model):
    _inherit = 'res.partner'

    es_administrador = fields.Boolean(string="Es Administrador")
    es_profesor = fields.Boolean(string="Es Profesor")
    es_apoderado = fields.Boolean(string="Es Apoderado")
    es_alumno = fields.Boolean(string="Es Alumno")
    token = fields.Char(string="Token", help="Token del Dispositivo")
    ci = fields.Char(string="Ci", help="Carnet de Identidad")

    cursos_ids = fields.One2many('agenda.curso', 'creador_id', string="Cursos")

    notificaciones_ids = fields.One2many('agenda.notificacion', 'creador_id', string="Notificaciones")

    materias_ids = fields.One2many('agenda.materia', 'creador_id', string="Materias")

    profesor_materia_ids = fields.One2many('agenda.profe.materia', 'profesor_id', string="Profesor Materias")

    materia_horarios_ids = fields.One2many('agenda.alumno.materia', 'alumno_id', string="Materia Horarios")

    tareas_ids = fields.One2many('agenda.tarea.alumno', 'alumno_id', string="Tareas")
    