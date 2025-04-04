from odoo import models, fields

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    unique_sku = fields.Char(string='SKU único')
    common_lot = fields.Char(string='Lote común')
    sku_prefix = fields.Char(string='Prefijo SKU')
