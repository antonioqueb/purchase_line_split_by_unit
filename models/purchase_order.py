from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'order_line' in vals:
                new_lines = []
                for index, line in enumerate(vals['order_line']):
                    command_type = line[0]
                    if command_type in [0, 1] and isinstance(line[2], dict):
                        data = line[2]
                        qty = int(data.get('quantity', 1))
                        product_id = data.get('product_id')
                        product = self.env['product.product'].browse(product_id)
                        if product and product.tracking == 'lot' and qty > 1:
                            for _ in range(qty):
                                single_line = data.copy()
                                single_line['quantity'] = 1
                                new_lines.append((0, 0, single_line))
                        else:
                            new_lines.append((0, 0, data))
                    else:
                        new_lines.append(line)
                vals['order_line'] = new_lines
        return super().create(vals_list)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.constrains('product_id')
    def _check_tracking_fields(self):
        for line in self:
            if line.product_id and line.product_id.tracking == 'lot':
                pass 
