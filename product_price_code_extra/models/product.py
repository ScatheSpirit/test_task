# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    honestus_code = fields.Char(
        string="Honestus Code",
        index=True
    )
    honestus_price = fields.Float(
        string="Honestus Price",
        digits="Product Price",
    )
