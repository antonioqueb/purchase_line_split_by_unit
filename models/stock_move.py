from odoo import models

class StockMove(models.Model):
    _inherit = 'stock.move'
    # Campo sku_prefix eliminado completamente
