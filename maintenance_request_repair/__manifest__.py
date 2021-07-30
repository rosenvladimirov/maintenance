# Copyright 2020 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Maintenance Request Repair',
    'summary': """
        This is a bridge module between Maintenance and Repair""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Maintenance',
    'author': 'Escodoo,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/maintenance',
    'depends': [
        'maintenance',
        'mrp_repair',
    ],
    'data': [
        'views/maintenance_request.xml',
        'views/mrp_repair_views.xml',
    ],
}
