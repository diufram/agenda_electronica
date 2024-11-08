{
    'name': "Agenda Electronica",
    'summary': "Sistema para Agenda Electronica de colegios",
    'description': """
        Es un sistema para que los colegios y sus estudiantes ocupen una agenda electrónica.
    """,
    'author': "Grupo 5",
    'category': 'Education',  # O prueba con una categoría más común en Odoo
    'version': '1.0',
    'depends': ['base'],  # Asegúrate de que 'hr' esté instalado si lo necesitas
    'data': [
        'security/ir.model.access.csv',
        'data/curso_seeder.xml',
        'data/horario_seeder.xml',
        'data/materia_seeder.xml',
        'data/materia_horario_seeder.xml',
        #'data/alumno_materia_seeder.xml',
        #'data/tarea_seeder.xml',
        #'data/tarea_alumno_seeder.xml',
        'data/persona_seeder.xml',
        #'data/apoderado_alumno_seeder.xml',
        'views/materia_view.xml',
        'views/curso_view.xml',
        #'views/persona_view.xml',
        'views/menu_view.xml',
        
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],  # Descomenta si tienes la imagen
    'installable': True,
    'application': True,
    'auto_install': False,
}
