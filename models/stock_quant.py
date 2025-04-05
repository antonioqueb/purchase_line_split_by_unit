# models/stock_quant.py
from odoo import models, fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    common_lot = fields.Char(string='Lote común')
    sku_prefix = fields.Char(string='Prefijo SKU')
