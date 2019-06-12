# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        if self.partner_id and self.order_line:
            self.order_line._onchange_product_id_for_customer_product_code()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_product_id = fields.Many2one('customer.product.code', ondelete='set null', string='Customer Product Code')
    customer_product_code = fields.Char('Customer Product Code (Code)', related='customer_product_id.name')

    @api.onchange('product_id', 'order_id')
    def _onchange_product_id_for_customer_product_code(self):
        for line in self:
            if line.product_id and line.order_id.partner_id and line.customer_product_id.product_id != line.product_id:
                customer_product_code_ids = self.env['customer.product.code'].search([('product_id', '=', line.product_id.id), ('partner_id', '=', line.order_id.partner_id.id)])
                if customer_product_code_ids:
                    line.customer_product_id = customer_product_code_ids[0]
                else:
                    line.customer_product_id = False

    @api.onchange('customer_product_id')
    def _onchange_customer_product_id(self):
        for line in self:
            if line.customer_product_id and line.order_id.partner_id and line.customer_product_id.product_id != line.product_id:
                line.product_id = line.customer_product_id.product_id

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({
            'customer_product_code': self.customer_product_code or self.product_id.default_code,
        })
        return res

    @api.multi
    def _prepare_procurement_values(self, group_id=False):

        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            'customer_product_code': self.customer_product_code or self.product_id.default_code,
        })
        return values



