from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    sku_unico = fields.Char(string="SKU Único", readonly=True)
    x_lote_comun = fields.Char(string='Lote común')
    x_sku_prefix = fields.Char(string='Prefijo SKU')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()

        for picking in self:
            line_counter = {}
            for move_line in picking.move_line_ids_without_package.filtered(lambda l: l.quantity == 1 and l.lot_id and not l.sku_unico):
                purchase_line = move_line.move_id.purchase_line_id
                if not purchase_line:
                    continue

                # Heredar campos a move_line
                move_line.x_lote_comun = purchase_line.x_lote_comun
                move_line.x_sku_prefix = purchase_line.x_sku_prefix

                prefix = move_line.x_sku_prefix or move_line.lot_id.name
                lot_name = move_line.lot_id.name

                if prefix not in line_counter:
                    line_counter[prefix] = 1
                else:
                    line_counter[prefix] += 1

                sku = f"{prefix}-{str(line_counter[prefix]).zfill(3)}"
                move_line.sku_unico = sku

        return res
