from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    unique_sku = fields.Char(string='SKU único')

    @api.model_create_multi
    def create(self, vals_list):
        move_lines = super().create(vals_list)
        for line in move_lines:
            if line.picking_id and line.picking_id.picking_type_code == 'incoming':
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.location_dest_id.id),
                    ('lot_id', '=', line.lot_id.id if line.lot_id else False),
                ])
                for quant in quants:
                    quant.unique_sku = line.unique_sku
        return move_lines
