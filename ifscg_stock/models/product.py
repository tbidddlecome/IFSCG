# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class CustomerProductCode(models.Model):
    _name = 'customer.product.code'
    _description = 'Customer Product Code'

    name = fields.Char('Customer Product Code', required=True)
    product_id = fields.Many2one('product.product', ondelete='set null', string='Product', required=True)
    partner_id = fields.Many2one('res.partner', ondelete='set null', string='Customer', required=True)

    _sql_constraints = [
        ('alias_uniq', 'UNIQUE(product_id, partner_id)',  _('Cannot create multiple alias for the same customer and the same product.')),
    ]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    customer_product_code_ids = fields.One2many('customer.product.code', 'product_id', string='Customer Product Code')
