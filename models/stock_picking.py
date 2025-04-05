# models/stock_picking.py

from odoo import models, api, fields, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        # Llamamos al proceso estándar
        res = super().button_validate()

        for picking in self:
            line_counter = {}
            # Se filtran líneas que tengan 1 unidad en el campo 'quantity'
            # y que no tengan todavía el unique_sku asignado.
            for move_line in picking.move_line_ids_without_package.filtered(
                lambda l: l.quantity == 1 and not l.unique_sku
            ):
                self._generate_sku_for_line(move_line, line_counter)

        return res

    def _generate_sku_for_line(self, move_line, line_counter):
        """Genera y asigna un SKU único a la línea y actualiza su Quant."""
        purchase_line = move_line.move_id.purchase_line_id
        if not purchase_line:
            return

        common_lot = purchase_line.common_lot
        sku_prefix = purchase_line.sku_prefix

        # Validaciones de campos de trazabilidad
        if not common_lot or not sku_prefix:
            raise UserError(_("Faltan datos de trazabilidad: asegúrese de definir 'Lote común' y 'Prefijo SKU'."))

        # Asignar datos a la línea
        move_line.common_lot = common_lot
        move_line.sku_prefix = sku_prefix

        # El campo lot_name provoca que Odoo genere un lote automáticamente
        move_line.lot_name = common_lot

        # Determinar el prefijo base (si sku_prefix está vacío, usar common_lot)
        prefix = sku_prefix or common_lot
        if not prefix:
            raise UserError(_("No se puede generar el SKU: no hay prefijo definido."))

        # Inicializar o incrementar el contador por prefijo
        if prefix not in line_counter:
            line_counter[prefix] = 1
        else:
            line_counter[prefix] += 1

        # Generar el SKU con un contador secuencial: PREFIX-001, PREFIX-002, etc.
        sku = f"{prefix}-{str(line_counter[prefix]).zfill(3)}"

        # Verificar que no exista ya el mismo SKU en este picking y producto
        existing = self.env['stock.move.line'].search_count([
            ('unique_sku', '=', sku),
            ('picking_id', '=', move_line.picking_id.id),
            ('product_id', '=', move_line.product_id.id),
        ])
        if existing:
            raise UserError(_(f"SKU duplicado detectado: {sku} ya existe en este albarán."))

        # Asignar el SKU en la línea de movimiento
        move_line.unique_sku = sku

        # Actualizar inmediatamente los Quants correspondientes
        quants = self.env['stock.quant'].search([
            ('product_id', '=', move_line.product_id.id),
            ('location_id', '=', move_line.location_dest_id.id),
            ('lot_id', '=', move_line.lot_id.id),
        ])
        for quant in quants:
            quant.unique_sku = sku
            quant.common_lot = common_lot
            quant.sku_prefix = sku_prefix
