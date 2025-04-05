from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    common_lot = fields.Char(string='Lote común', related='purchase_line_id.common_lot', store=True, readonly=False)
    sku_prefix = fields.Char(string='Prefijo SKU', related='purchase_line_id.sku_prefix', store=True, readonly=False)
