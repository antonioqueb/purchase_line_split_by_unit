# models/stock_production_lot.py
from odoo import models, fields

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    common_lot = fields.Char(string='Lote común')
    sku_prefix = fields.Char(string='Prefijo SKU')
