# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    asset_id = fields.Many2one('account.asset', 'Linked Account Asset')

    @api.onchange('asset_id')
    def _onchange_asset_id(self):
        for record in self:
            if record.asset_id and not record.asset_id.maintenance_equipment_id:
                record.asset_id.maintenance_equipment_id = record.id
