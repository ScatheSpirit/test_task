# -*- coding: utf-8 -*-

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # I wrote this function based on the task: Task 3. Update Order/Quotation report
    # It says nothing about the need to change the name generation (display_name)
    # in the 'sale.order.line' object itself, what seemed strange, but only on the printed form
    def get_line_name_for_honestus_report(self):
        """
        The function returns a custom line name for the honestus modified report 'Quotation / Order'
        :return:  (str) custom line name
        """
        for line in self:
            default_code = line.product_id.default_code
            honestus_code = line.product_id.honestus_code
            honestus_name = line.name

            if honestus_code:
                if default_code and "[{}]".format(default_code) in honestus_name:
                    honestus_name = line.name.replace(
                        "[{}]".format(default_code),
                        "[{}]".format(honestus_code)
                    )
                else:
                    honestus_name = "[{}] {}".format(honestus_code, honestus_name)

            return honestus_name

    # This function has been redefined only for recalculating prices for a report. ONLY WITHIN THE TASK!
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        if self.env.context.get('honestus_price', False):
            for line in self:
                if line.product_id.honestus_price:
                    price = line.product_id.honestus_price * (1 - (line.discount or 0.0) / 100.0)
                else:
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)

                taxes = line.tax_id.compute_all(
                    price,
                    line.order_id.currency_id,
                    line.product_uom_qty,
                    product=line.product_id,
                    partner=line.order_id.partner_shipping_id
                )
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
                if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                        'account.group_account_manager'):
                    line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
        else:
            super(SaleOrderLine, self)._compute_amount()
