from odoo import api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

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
                    quant.common_lot = line.common_lot
                    quant.sku_prefix = line.sku_prefix
        return move_lines
