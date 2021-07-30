# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    mrp_repair_order_id = fields.Many2one('mrp.repair', 'Repair Order')
