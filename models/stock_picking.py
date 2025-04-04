from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    sku_unico = fields.Char(string="SKU Único", readonly=True)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()

        for picking in self:
            line_counter = {}
            for move_line in picking.move_line_ids_without_package.filtered(lambda l: l.qty_done == 1 and l.lot_id and not l.sku_unico):
                purchase_line = move_line.move_id.purchase_line_id
                prefix = purchase_line.x_sku_prefix or move_line.lot_id.name
                lot_name = move_line.lot_id.name

                if prefix not in line_counter:
                    line_counter[prefix] = 1
                else:
                    line_counter[prefix] += 1

                sku = f"{prefix}-{str(line_counter[prefix]).zfill(3)}"
                move_line.sku_unico = sku

        return res
