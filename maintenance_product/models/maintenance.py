# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):
    _inherit = ['maintenance.equipment']
    _name = 'maintenance.equipment'
    _inherits = {'product.product': 'product_id', }
    _order = 'assign_date desc'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'

    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the equipment without removing it.")

    product_id = fields.Many2one('product.product', string='Base on Product', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('product.template'), index=1)

    parent_id = fields.Many2one('maintenance.equipment', 'Parent Equipment',
                                index=True, ondelete='cascade',
                                track_visibility='onchange',)
    child_ids = fields.One2many('maintenance.equipment', 'parent_id',
                                'Child Equipments')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)
    child_count = fields.Integer(
        compute='_compute_child_count',
        string="Number of child equipments")
    display_name = fields.Char(compute='_compute_display_name')
    complete_name = fields.Char(compute='_compute_complete_name', store=True)
    lot_id = fields.Many2one('stock.production.lot', 'Lot')
    use_date = fields.Datetime(string='Best before Date', related="lot_id.use_date")
    warranty_date = fields.Datetime(string='Warranty Date', related="lot_id.warranty_date")
    location_id = fields.Many2one('stock.location', 'Location', ondelete='restrict')
    quant_ids = fields.One2many('stock.quant', string='Quants', related="lot_id.quant_ids", readonly=True)
    location_ids = fields.One2many('stock.location', string="Locatons", compute="_compute_locations_ids")

    # maintenance_product_properties moved
    manufacturer_id = fields.Many2one('res.partner', string='Manufacturer', related="product_id.manufacturer_id", readonly=True)

    @api.multi
    def _compute_locations_ids(self):
        for record in self:
            if record.lot_id:
                record.location_ids = False
                for line in record.quant_ids:
                    if line.location_id.usage == 'internal':
                        record.location_ids |= line.location_id

    #def name_get(self):
    #    return [(equipment.id, equipment.complete_name) for equipment in self]

    @api.depends('child_ids')
    def _compute_child_count(self):
        for equipment in self:
            equipment.child_count = len(equipment.child_ids)

    def _compute_display_name(self):
        for equipment in self:
            equipment.display_name = equipment.complete_name

    @api.depends('name', 'parent_id.complete_name')  # recursive definition
    def _compute_complete_name(self):
        for equipment in self:
            if equipment.parent_id:
                parent_name = equipment.parent_id.complete_name
                equipment.complete_name = parent_name + ' / ' + equipment.name
            else:
                equipment.complete_name = equipment.name

    @api.constrains('parent_id')
    def _check_equipment_recursion(self):
        if not self._check_recursion():
            raise ValidationError(
                _('Error ! You cannot create a recursive '
                  'equipment hierarchy.'))
        return True

    @api.depends('name')
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.with_context(dict(self._context, display_default_code=False)).display_name
            self.lot_id = False
            self.serial_no = False

    @api.depends('serial_no')
    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        if self.lot_id:
            self.serial_no = self.lot_id.name

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.product_id and record.serial_no:
                result.append((record.id, record.product_id.with_context(dict(self._context, display_default_code=True)).display_name + '/' + record.serial_no))
            if record.product_id and not record.serial_no:
                result.append((record.id, record.product_id.with_context(dict(self._context, display_default_code=True)).display_name))
        return result

    def preview_child_list(self):
        return {
            'name': 'Child equipment of %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'res_id': self.id,
            'view_mode': 'list,form',
            'context': {
                **self.env.context,
                'default_parent_id': self.id,
                'parent_id_editable': False},
            'domain': [('id', 'in', self.child_ids.ids)],
        }
