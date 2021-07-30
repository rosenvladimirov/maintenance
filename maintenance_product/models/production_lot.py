# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    warranty_date = fields.Datetime(string='Warranty Date',
        help='This is the date on which the goods with this Serial Number of end warranty.')
