from odoo import models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'order_line' in vals:
                new_lines = []
                for line in vals['order_line']:
                    command_type = line[0]
                    if command_type in [0, 1] and isinstance(line[2], dict):
                        qty = int(line[2].get('quantity', 1))
                        product_id = line[2].get('product_id')
                        if product_id:
                            product = self.env['product.product'].browse(product_id)
                            if product.tracking == 'lot' and qty > 1:
                                for i in range(qty):
                                    single_line = line[2].copy()
                                    single_line['quantity'] = 1
                                    new_lines.append((0, 0, single_line))
                            else:
                                new_lines.append(line)
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                vals['order_line'] = new_lines
        return super().create(vals_list)