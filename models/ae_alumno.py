from odoo import models, fields, api

class Alumno(models.Model):
    _name = 'agenda.alumno'
    _inherits = {'res.users': 'user_id'}
    _description = 'Modelo para personas en la agenda'

    ci = fields.Char(string="CI", help="Carnet de Identidad")
    token = fields.Char(string="Token", help="Token del Dispositivo")
    user_id = fields.Many2one('res.users', required=True, ondelete="cascade")

    apoderado_ids = fields.One2many('agenda.apoderado.alumno', 'alumno_id', string="Apoderados a Cargo")
    asistencia_ids = fields.One2many('agenda.asistencia.alumno', 'alumno_id', string="Asistencias")
    tareas_ids = fields.One2many('agenda.tarea.alumno', 'alumno_id', string="Tareas")
    cursos_ids = fields.One2many('agenda.alumno.curso', 'alumno_id', string="Cursos del Alumno")

    @api.model_create_multi
    def create(self, vals_list):
        """Sobrescribe el método create para manejar múltiples registros."""
        for vals in vals_list:
            if 'user_id' not in vals:
                # Crear un usuario relacionado si no se especifica user_id
                user_vals = {
                    'name': vals.get('name', 'Alumno Sin Nombre'),
                    'login': vals.get('login', f"alumno_{len(vals_list)}@example.com"),
                    'groups_id': [(4, self.env.ref('agenda_electronica.group_alumno').id)],  # Asignar al grupo de alumnos
                }
                user = self.env['res.users'].create(user_vals)
                vals['user_id'] = user.id

        # Llama al método original para procesar los registros
        return super(Alumno, self).create(vals_list)
