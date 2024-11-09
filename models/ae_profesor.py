from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'agenda.profesor'
    _inherits = {'res.users': 'user_id'}
    _description = 'Modelo para personas en la agenda'

    ci = fields.Char(string="CI", help="Carnet de Identidad")
    token = fields.Char(string="Token", help="Token del Dispositivo")
    user_id = fields.Many2one('res.users', required=True, ondelete="cascade")
    materia_horario_ids = fields.One2many('agenda.materia.horario', 'profesor_id', string="Materias y Horarios")

    @api.model_create_multi
    def create(self, vals_list):
        """Sobrescribe el método create para manejar múltiples registros."""
        for vals in vals_list:
            if 'user_id' not in vals:
                # Crear un usuario relacionado si no se especifica user_id
                user_vals = {
                    'name': vals.get('name', 'Profesor Sin Nombre'),
                    'login': vals.get('login', f"profesor_{len(vals_list)}@example.com"),
                    'groups_id': [(4, self.env.ref('agenda_electronica.group_profesor').id)],  # Asignar al grupo de profesores
                }
                user = self.env['res.users'].create(user_vals)
                vals['user_id'] = user.id

        # Llama al método original para procesar los registros
        return super(Profesor, self).create(vals_list)
