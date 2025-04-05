from odoo import models, api, fields, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        for picking in self:
            line_counter = {}
            for move_line in picking.move_line_ids_without_package.filtered(
                lambda l: l.quantity == 1 and not l.unique_sku
            ):
                self._generate_sku_for_line(move_line, line_counter)
        return res

    def _generate_sku_for_line(self, move_line, line_counter):
        if not move_line.lot_id:
            raise UserError(_("Debe asignar un lote (lot_id) en cada línea de recepción."))

        lot_name = move_line.lot_id.name
        if not lot_name:
            raise UserError(_("El lote asignado no tiene nombre (lot_id.name)."))

        if lot_name not in line_counter:
            line_counter[lot_name] = 1
        else:
            line_counter[lot_name] += 1

        sku = f"{lot_name}-{str(line_counter[lot_name]).zfill(3)}"

        existing = self.env['stock.move.line'].search_count([
            ('unique_sku', '=', sku),
            ('picking_id', '=', move_line.picking_id.id),
            ('product_id', '=', move_line.product_id.id),
        ])
        if existing:
            raise UserError(_(f"SKU duplicado detectado: {sku} ya existe en este albarán."))

        move_line.unique_sku = sku

        quants = self.env['stock.quant'].search([
            ('product_id', '=', move_line.product_id.id),
            ('location_id', '=', move_line.location_dest_id.id),
            ('lot_id', '=', move_line.lot_id.id),
        ])
        for quant in quants:
            quant.unique_sku = sku
