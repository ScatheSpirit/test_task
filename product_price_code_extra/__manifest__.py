# -*- coding: utf-8 -*-
{
    "name": "Extra Price & Code in Product",
    "summary": "Extra Price and Product Code. Order Line Report",
    "description": """
            This module adds an extra code and price to a product.product ('Honestus Code' and 'Honestus Price').
            In Order/Quotation report, it replaces standard Default Code and Unit Price with extra ones.
            Adds Order Line Analysis report to the Sales -> Reporting menu, taking into account extra fields.
        """,
    "author": "Oleksii Panin",
    "version": "14.0.1.0.0",
    "category": "Sales/Sales",
    "license": "LGPL-3",
    "depends": [
        "sale_management"
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/sale_report_views.xml",
        "views/product_views.xml",
        "views/sale_report_templates.xml"
    ],
    "installable": True,
}
