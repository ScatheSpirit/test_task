# -*- coding: utf-8 -*-

from odoo import tools
from odoo import fields, models


class SaleOrderLineReport(models.Model):
    _name = "sale.order.line.report"
    _description = "Sales Order Line Analysis Report"
    _auto = False

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        readonly=True
    )
    name = fields.Char(
        string="Order Reference",
        readonly=True
    )
    product_code = fields.Char(
        string="Product Code",
        readonly=True
    )
    product_honestus_code = fields.Char(
        string="Honestus Code",
        readonly=True
    )
    price_unit = fields.Float(
        string="Unit Price",
        readonly=True
    )
    price_honestus = fields.Float(
        string="Honestus Price",
        readonly=True
    )
    margin = fields.Float(
        string="Margin",
        readonly=True
    )

    def _select(self):
        return """
            SELECT
                sol.id AS id, 
                rp.id AS partner_id, 
                so.name AS name, 
                pp.default_code AS product_code, 
                pp.honestus_code AS product_honestus_code, 
                sol.price_unit AS price_unit, 
                pp.honestus_price AS price_honestus, 
                CASE 
                    WHEN pp.honestus_price IS NOT NULL THEN (pp.honestus_price - pt.list_price) / pp.honestus_price
                    WHEN pp.honestus_price IS NULL THEN (sol.price_unit - pt.list_price) / sol.price_unit
                END as margin    
        """

    def _from(self):
        return """
            FROM sale_order_line AS sol
        """

    def _join(self):
        return """
            RIGHT OUTER JOIN sale_order AS so ON so.id = sol.order_id
            JOIN res_partner AS rp on so.partner_id = rp.id
            LEFT JOIN product_product AS pp ON sol.product_id = pp.id
            LEFT JOIN product_template AS pt on pp.product_tmpl_id = pt.id
        """

    def _where(self):
        return """
            WHERE sol.display_type IS NULL
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._join(), self._where())
        )
