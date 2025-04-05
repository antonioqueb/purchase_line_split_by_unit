# models/stock_quant.py
from odoo import models, fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    unique_sku = fields.Char(string='SKU único')
    common_lot = fields.Char(string='Lote común')
    sku_prefix = fields.Char(string='Prefijo SKU')
