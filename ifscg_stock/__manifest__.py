# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'IFSCG: Customer Product Code',
    'summary': 'Customer Product Code',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '2.0',
    'author': 'Odoo Inc',
    'description': """
Various customers call the same product differently.
Let's the product ITALIAN STYLE MEATBALLS 1 OZ MAC has Internal reference as 001
Customer A has an internal reference 20265
Customer B has an internal reference 20001
So in the SO to Customer A, when we select the product "ABC123", it should auto-populate the internal reference as 20265.
If customer C buys this product it will have internal reference 001.
In the database create a Model called Customer Product Code. This model will have the following fields - Customer Product Code, product name and Customer.
When I create the Invoice and Delivery Order, this reference should pass on to the invoice and Delivery Order Form with the new reference number.
    """,
    'category': 'Custom Development',
    'depends': ['sale_management', 'delivery', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_product_code.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/account_invoice.xml',
        'views/stock_picking.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
