from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    common_lot = fields.Char(string='Lote común')
    sku_prefix = fields.Char(string='Prefijo SKU')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            lote = vals.get('common_lot')
            sku_prefix = vals.get('sku_prefix')

            if 'order_line' in vals:
                new_lines = []
                for line in vals['order_line']:
                    command_type = line[0]
                    if command_type in [0, 1] and isinstance(line[2], dict):
                        data = line[2]
                        qty = int(data.get('quantity', 1))
                        product_id = data.get('product_id')
                        product = self.env['product.product'].browse(product_id)
                        if product and product.tracking == 'lot' and qty > 1:
                            for i in range(qty):
                                single_line = data.copy()
                                single_line['quantity'] = 1
                                if lote:
                                    single_line['common_lot'] = lote
                                if sku_prefix:
                                    single_line['sku_prefix'] = sku_prefix
                                new_lines.append((0, 0, single_line))
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                vals['order_line'] = new_lines
        return super().create(vals_list)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    common_lot = fields.Char(string='Lote común')
    sku_prefix = fields.Char(string='Prefijo SKU')

    @api.constrains('product_id', 'common_lot', 'sku_prefix')
    def _check_tracking_fields(self):
        for line in self:
            if line.product_id and line.product_id.tracking == 'lot':
                if not line.common_lot or not line.sku_prefix:
                    raise ValidationError("Debe asignar lote común y prefijo de SKU en productos con trazabilidad por lote.")
