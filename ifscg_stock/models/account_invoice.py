# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(AccountInvoice, self)._onchange_partner_id()
        if self.partner_id and self.invoice_line_ids:
            self.invoice_line_ids._onchange_product_id_for_customer_product_code()


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    customer_product_code = fields.Char('Customer Product Code')

    @api.onchange('product_id', 'invoice_id')
    def _onchange_product_id_for_customer_product_code(self):
        for line in self:
            if line.product_id and line.invoice_id.partner_id:
                customer_product_code_ids = self.env['customer.product.code'].search([('product_id', '=', line.product_id.id), ('partner_id', '=', line.invoice_id.partner_id.id)])
                if customer_product_code_ids:
                    line.customer_product_code = customer_product_code_ids[0].name
                else:
                    line.customer_product_code = line.product_id.default_code


