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
        Lot = self.env['stock.production.lot']
        StockMoveLine = self.env['stock.move.line']

        purchase_line = move_line.move_id.purchase_line_id
        if not purchase_line:
            return

        common_lot = purchase_line.common_lot
        sku_prefix = purchase_line.sku_prefix

        if not common_lot or not sku_prefix:
            raise UserError(_("Faltan datos de trazabilidad: asegúrese de definir 'Lote común' y 'Prefijo SKU'."))

        # Asignar datos a la línea
        move_line.common_lot = common_lot
        move_line.sku_prefix = sku_prefix

        # Buscar o crear el lote
        lot_id = Lot.search([
            ('name', '=', common_lot),
            ('product_id', '=', move_line.product_id.id)
        ], limit=1)

        if not lot_id:
            lot_id = Lot.create({
                'name': common_lot,
                'product_id': move_line.product_id.id
            })

        move_line.lot_id = lot_id

        # Determinar prefijo base
        prefix = sku_prefix or lot_id.name
        if not prefix:
            raise UserError(_("No se puede generar el SKU: no hay prefijo definido."))

        # Inicializar contador
        if prefix not in line_counter:
            line_counter[prefix] = 1
        else:
            line_counter[prefix] += 1

        # Generar SKU
        sku = f"{prefix}-{str(line_counter[prefix]).zfill(3)}"

        # Validar duplicado (opcional: por picking y producto)
        existing = StockMoveLine.search_count([
            ('unique_sku', '=', sku),
            ('picking_id', '=', move_line.picking_id.id),
            ('product_id', '=', move_line.product_id.id),
        ])
        if existing:
            raise UserError(_(f"SKU duplicado detectado: {sku} ya existe en este albarán."))

        move_line.unique_sku = sku
