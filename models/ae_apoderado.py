from odoo import models, fields, api

class Apoderado(models.Model):
    _name = 'agenda.apoderado'
    _inherits = {'res.users': 'user_id'}
    _description = 'Modelo para personas en la agenda'

    ci = fields.Char(string="CI", help="Carnet de Identidad")
    token = fields.Char(string="Token", help="Token del Dispositivo")
    user_id = fields.Many2one('res.users', required=True, ondelete="cascade")
    alumno_ids = fields.One2many('agenda.apoderado.alumno', 'apoderado_id', string="Alumnos a Cargo")

    @api.model_create_multi
    def create(self, vals_list):
        """Sobrescribe el método create para manejar múltiples registros."""
        for vals in vals_list:
            if 'user_id' not in vals:
                # Crear un usuario relacionado si no se especifica user_id
                user_vals = {
                    'name': vals.get('name', 'Apoderado Sin Nombre'),
                    'login': vals.get('login', f"apoderado_{len(vals_list)}@example.com"),
                    'groups_id': [(4, self.env.ref('agenda_electronica.group_apoderado').id)],  # Asignar al grupo de apoderados
                }
                user = self.env['res.users'].create(user_vals)
                vals['user_id'] = user.id

        # Llama al método original para procesar los registros
        return super(Apoderado, self).create(vals_list)
