from odoo import models, fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    unique_sku = fields.Char(string='SKU único')
