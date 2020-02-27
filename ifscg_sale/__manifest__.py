# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'IFSCG Sale',
    'category': 'Custom Development',
    'sequence': 60,
    'summary': 'IFSCG Calculate Qty on Sale',
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'depends': ['sale_management', 'purchase', 'account', 'stock', 'ifscg_stock'],
    'version': '1.0',
    'description': """
IFSCG Calculate Qty
===================
* [#1959395]

* Req 1:
    - Create a new field "Weight for SO" on the product. (Default this to 1)
    -  Add a new column called cases on the SO Line.
    - Ordered qty will be calculated by the formula (case * weight for SO)
    - The SO line will have the new column and Ordered qty will be calculated based on that -
    - Since Case is 5, this gets multiplied by the weight which gets the ordered qty to 108.1.
    - If someone modifies the ordered qty,
    - give a pop-up warning saying that "Adjust case qty as per ordered qty"

* Req 2:
    - Add a calculated field called "Volume" on the Invoice Form and PO Form.
    - Volume = Case (filed on invoice and PO) * volume (field on the product)
""",
    'data': [

        # views
        'data/data.xml',
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/invoice_views.xml',

    ],
    'test': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
