# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Maintenance product link",
    "version" : "11.0.1.0",
    "author" : "Rosen Vladimirov, Bioprint Ltd.",
    'category': 'Equipments, Assets, Internal Hardware, Allocation Tracking',
    "description": """
    """,
    'conflicts': [
        'maintenance_equipment_hierarchy'
    ],
    'depends': [
        'maintenance',
        'stock',
        'product_expiry',
        'product_properties',
    ],
    "demo" : [],
    "data" : [
        'views/maintenance_equipment_views.xml',
        'views/production_lot_views.xml',
          ],
    "license": "AGPL-3",
    "installable": True,
}
