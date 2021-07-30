# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    maintenance_equipment_id = fields.Many2one(
        comodel_name='maintenance.equipment',
        string='Equipment',
        help='If this asset is maintenance equipment choice or crete it.'
    )

    @api.onchange('maintenance_equipment_id')
    def _onchange_maintenance_equipment_id(self):
        for record in self:
            if record.maintenance_equipment_id and not record.maintenance_equipment_id.asset_id:
                record.maintenance_equipment_id.asset_id = record.id

    def _create_maintenance_equipment(self):
        return {
            'company_id': self.company_id.id,
            'product_id': self.product_id.id,
            'lot_id': self.lot_id.id,
            'asset_id': self.id,
            'partner_id': self.partner_id.id,
            'cost': self.purchase_value,
            'name': self.name,
            'assign_date': self.date_start,
            'manufacturer_id': self.product_id.manufacturer_id and self.product_id.manufacturer_id.id or False
        }

    @api.multi
    def create_maintenance_equipment(self):
        for record in self:
            if record.type == 'normal':
                equipment = self.env['maintenance.equipment'].create(record._create_maintenance_equipment())
                if equipment:
                    record.maintenance_equipment_id = equipment
                if record.parent_id:
                    record.parent_id.create_maintenance_equipment()

    @api.multi
    def validate(self):
        for record in self:
            if record and record.maintenance_equipment_id and \
                ((record.state == 'draft' and self._context.get('asset_out')) or
                 record.state == 'close' or not record.active):
                record.maintenance_equipment_id.active = False
        return super(AccountAsset, self).validate()
