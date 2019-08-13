# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    weight_for_so = fields.Float(
        'Weight For So', compute='_compute_weight_for_so', digits=dp.get_precision('Stock Weight'),
        inverse='_set_weight_for_so', store=True, default=1)

    @api.one
    def _set_weight_for_so(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.weight_for_so = self.weight_for_so

    @api.depends('product_variant_ids', 'product_variant_ids.weight_for_so')
    def _compute_weight_for_so(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.weight_for_so = template.product_variant_ids.weight_for_so
        for template in (self - unique_variants):
            template.weight_for_so = 1


class ProductProduct(models.Model):
    _inherit = "product.product"

    weight_for_so = fields.Float(string="Weight For So", digits=dp.get_precision('Stock Weight'), default=1)
