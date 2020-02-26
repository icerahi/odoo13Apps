{
    'name': "VISITOR LOG BOOK",

    'summary': """
        Custom Odoo module for Initial practice by Rahi""",

    'description': """
        Simple working for practice and learning
    """,

    'author': "Imran Hasan",
    'website': "https://www.fb.com/icerahi/",
    'category': 'Tools',
    'version': '1.0',
    'depends': [
        'base',
        'mail',


    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/appointment.xml',
        'views/employee.xml',
        'views/visitor.xml',
        'views/check_in_out.xml',


    ],
    'license': "",
    'installable': True,
    'application': True,
    'sequence': 1,
}
