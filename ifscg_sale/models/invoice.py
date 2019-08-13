# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)
    case = fields.Float(string="Cases")

    @api.onchange('case', 'product_id')
    def onchange_case(self):
        self.quantity = self.case * self.product_id.weight_for_so
        # product_uom_case = self.env.ref('ifscg_sale.product_uom_case').id
        # product_uom_pound = self.env.ref('ifscg_sale.product_uom_pound').id
        # self.uom_id = self.product_id.weight_for_so > 1 and product_uom_pound or product_uom_case

    @api.one
    @api.constrains('case', 'quantity')
    def validate_ordered_qty(self):
        quantity = self.case * self.product_id.weight_for_so
        if self.case > 0 and self.quantity != quantity:
            raise ValidationError(_('The calculated ordered quantity has been modified, if you need to recalculate the ordered quantity then you have to modify the Cases value'))

    @api.depends('case', 'product_id', 'product_id.volume')
    def _compute_volume(self):
        for rec in self:
            rec.volume = rec.case * rec.product_id.volume


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        data = super(AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        data['case'] = line.case
        data['volume'] = line.volume
        return data
