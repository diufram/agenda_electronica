from odoo import models, fields

class Persona(models.Model):
    _inherit = 'res.partner'

    es_administrador = fields.Boolean(string="Es Administrador")
    es_profesor = fields.Boolean(string="Es Profesor")
    es_apoderado = fields.Boolean(string="Es Apoderado")
    es_alumno = fields.Boolean(string="Es Alumno")
    token = fields.Char(string="Token", help="Token del Dispositivo")
    ci = fields.Char(string="Ci", help="Carnet de Identidad")

    alumno_ids = fields.Many2many(
        'res.partner',  # Modelo relacionado (res.partner)
        'apododerado_alumno',  # Nombre de la tabla intermedia
        'apoderado_id',  # Columna que representa al apoderado en la tabla intermedia
        'alumno_id',  # Columna que representa al alumno en la tabla intermedia
        string="Alumnos",
        domain=[('es_alumno', '=', True)]  # Filtro para mostrar solo alumnos
    )

    apoderado_ids = fields.Many2many(
        'res.partner',
        'apododerado_alumno',
        'alumno_id',  # Columna que representa al alumno en la tabla intermedia
        'apoderado_id',  # Columna que representa al apoderado en la tabla intermedia
        string="Apoderados",
        domain=[('es_apoderado', '=', True)]  # Filtro para mostrar solo apoderados
    )


    notificaciones_ids = fields.One2many('agenda.notificacion', 'creador_id', string="Notificaciones")

    profesor_materia_ids = fields.One2many('agenda.profe.materia', 'profesor_id', string="Profesor Materias")

    materia_horarios_ids = fields.One2many('agenda.alumno.materia', 'alumno_id', string="Materia Horarios")

    tareas_ids = fields.One2many('agenda.tarea.alumno', 'alumno_id', string="Tareas")
    