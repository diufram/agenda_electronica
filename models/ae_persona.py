from odoo import models, fields

class Persona(models.Model):
    _inherit = 'res.users'

    es_administrador = fields.Boolean(string="Es Administrador")
    es_profesor = fields.Boolean(string="Es Profesor")
    es_apoderado = fields.Boolean(string="Es Apoderado")
    es_alumno = fields.Boolean(string="Es Alumno")
    token = fields.Char(string="Token", help="Token del Dispositivo")
    ci = fields.Char(string="Ci", help="Carnet de Identidad")
    name = fields.Char(string="Nombre")

    alumno_ids = fields.One2many('agenda.apoderado.alumno', 'alumno_id', string="Alumno")

    apoderado_ids = fields.One2many('agenda.apoderado.alumno', 'apoderado_id', string="Apoderado")


    notificaciones_ids = fields.One2many('agenda.notificacion', 'creador_id', string="Notificaciones")

    materia_horario_ids = fields.One2many('agenda.materia.horario', 'profesor_id', string="Profesor Materias")

    materia_horarios_ids = fields.One2many('agenda.alumno.materia', 'alumno_id', string="Materia Horarios")

    tareas_ids = fields.One2many('agenda.tarea.alumno', 'alumno_id', string="Tareas")

    asistencia_alumno_ids = fields.One2many('agenda.asistencia.alumno', 'alumno_id', string="Asistencias")
    