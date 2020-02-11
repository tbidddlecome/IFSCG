# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    volume = fields.Float(string="Volume", compute="_compute_product_info", store=True)
    total_weight = fields.Float(string="Total Weight", compute="_compute_product_info", store=True)
    case = fields.Float(string="Cases")

    @api.onchange('case', 'product_id')
    def onchange_case(self):
        self.product_qty = self.case * self.product_id.weight_for_so
        # product_uom_case = self.env.ref('ifscg_sale.product_uom_case').id
        # product_uom_pound = self.env.ref('ifscg_sale.product_uom_pound').id
        # self.product_uom = self.product_id.weight_for_so > 1 and product_uom_pound or product_uom_case

    @api.onchange('product_qty', 'case')
    def onchange_product_qty_case(self):
        # product_uom_qty = self.case * self.product_id.weight_for_so
        if self.case > 0 and self.product_qty != self.case * self.product_id.weight_for_so:
            warning_mess = {
                'title': _('Warning'),
                'message': _('The calculated ordered quantity has been modified, if you need to recalculate the ordered quantity then you have to modify the Cases value') 
            }
            return {'warning': warning_mess}
        return {}
        
    @api.depends('case', 'product_id', 'product_id.volume', 'product_id.weight')
    def _compute_product_info(self):
        for rec in self:
            rec.volume = rec.case * rec.product_id.volume
            rec.total_weight = rec.case * rec.product_id.weight
