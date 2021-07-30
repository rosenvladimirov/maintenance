# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Maintenance assents link",
    "version": "11.0.1.0",
    "author": "Rosen Vladimirov, Bioprint Ltd.",
    'category': 'Equipments, Assets, Internal Hardware, Allocation Tracking',
    "description": """
    """,
    'conflicts': [
        'maintenance_equipment_hierarchy'
    ],
    'depends': [
        'account_asset_management',
        'maintenance',
        'maintenance_product',
    ],
    "demo": [],
    "data": [
        "views/account_asset.xml",
        "views/maintenance_equipment_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
