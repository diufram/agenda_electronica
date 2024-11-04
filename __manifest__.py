{
    'name': "Agenda Electronica",
    'summary': "Sistema para Agenda Electronica de colegios",
    'description': """
        Es un sistema para que los colegios y sus estudiantes ocupen una agenda electrónica.
    """,
    'author': "Grupo5",
    'category': 'Education',  # O prueba con una categoría más común en Odoo
    'version': '1.0',
    'depends': ['base', 'hr'],  # Asegúrate de que 'hr' esté instalado si lo necesitas
    'data': [
        'security/ir.model.access.csv',
        'data/curso_seeder.xml',
        'data/horario_seeder.xml',
        'data/materia_seeder.xml',
        'data/materia_horario_seeder.xml',
        'data/alumno_materia_seeder.xml',
        'data/tarea_seeder.xml',
        'data/tarea_alumno_seeder.xml',
    ],
    'license': 'LGPL-3',
    # 'images': ['static/description/banner.gif'],  # Descomenta si tienes la imagen
    'installable': True,
    'application': True,
    'auto_install': False,
}
