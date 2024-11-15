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
        'security/grupos.xml',
        'security/ir.model.access.csv',
        #'security/reglas.xml',
        'data/curso_seeder.xml',
        'data/administrador_seeder.xml',
        'data/horario_seeder.xml',
        'data/materia_seeder.xml',
        'data/alumno_seeder.xml',
        'data/profesor_seeder.xml',
        'data/apoderado_seeder.xml',
        'data/materia_horario_seeder.xml',
        'data/alumno_curso_seeder.xml',
        'data/apoderado_alumno_seeder.xml',

        'views/materia_view.xml',
        'views/curso_view.xml',
        #'views/mis_materias.xml',
        'views/alumno_views.xml',
        'views/ae_horario_views.xml',
        'views/apoderado_views.xml',
        'views/profesor_views.xml',
        'views/ae_materia_horario_views.xml',
        'views/alumno_curso_views.xml',
        'views/ae_apoderado_alumno_views.xml',
        'views/materia_asignada_profesor_views.xml',
        'views/menu_view.xml',  
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],  # Descomenta si tienes la imagen
    'installable': True,
    'application': True,
    'auto_install': False,
}
