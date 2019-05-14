# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):

        move_values = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
        move_values.update({
            'customer_product_code': values.get('customer_product_code')
        })

        return move_values


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        super(StockPicking, self).onchange_picking_type()
        if self.partner_id and self.move_ids_without_package:
            self.move_ids_without_package._onchange_product_id_for_customer_product_code()


class StockMove(models.Model):
    _inherit = 'stock.move'

    customer_product_code = fields.Char('Customer Product Code')

    @api.onchange('product_id', 'picking_id')
    def _onchange_product_id_for_customer_product_code(self):
        for move in self:
            if move.product_id and move.picking_id and move.picking_id.partner_id:

                customer_product_code_ids = self.env['customer.product.code'].search(
                    [('product_id', '=', move.product_id.id), ('partner_id', '=', move.picking_id.partner_id.id)])
                if customer_product_code_ids:
                    move.customer_product_code = customer_product_code_ids[0].name
                else:
                    move.customer_product_code = move.product_id.default_code


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    customer_product_code = fields.Char(related='move_id.customer_product_code')