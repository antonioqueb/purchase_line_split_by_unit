from odoo import models, fields

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    sku_unico = fields.Char(string='SKU único')  # Campo técnico generado
    x_lote_comun = fields.Char(string='Lote común')  # Campo editable heredado de líneas de compra
    x_sku_prefix = fields.Char(string='Prefijo SKU')  # Campo editable heredado de líneas de compra
