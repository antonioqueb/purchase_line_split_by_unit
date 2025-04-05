# models/stock_quant.py
from odoo import models, fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    common_lot = fields.Char(string='Lote común', related='lot_id.common_lot', store=True)
    sku_prefix = fields.Char(string='Prefijo SKU', related='lot_id.sku_prefix', store=True)
