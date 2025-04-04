# models/stock_picking.py
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()

        # (1) Creamos un objeto que usaremos para buscar o crear los lotes
        Lot = self.env['stock.production.lot']

        for picking in self:
            line_counter = {}

            # Filtramos las move lines de 1 en 1 que no tengan sku_unico todavía
            for move_line in picking.move_line_ids_without_package.filtered(lambda l: l.quantity == 1 and not l.sku_unico):
                purchase_line = move_line.move_id.purchase_line_id
                if not purchase_line:
                    continue

                # a) Tomar el 'lote común' y prefijo definidas en la línea de compra
                lote_comun = purchase_line.x_lote_comun
                sku_prefix = purchase_line.x_sku_prefix

                # b) Asignar campos X_ a la move line (como hacías antes)
                move_line.x_lote_comun = lote_comun
                move_line.x_sku_prefix = sku_prefix

                # c) Buscar o crear el lot_id si existe un x_lote_comun
                #    Evitamos crear lote si lote_comun está vacío.
                lot_id = False
                if lote_comun:
                    lot_id = Lot.search([
                        ('name', '=', lote_comun),
                        ('product_id', '=', move_line.product_id.id)
                    ], limit=1)
                    if not lot_id:
                        lot_id = Lot.create({
                            'name': lote_comun,
                            'product_id': move_line.product_id.id,
                        })
                
                # d) Asignar el lot_id a la move_line
                if lot_id:
                    move_line.lot_id = lot_id

                # e) Determinar el prefijo para el SKU
                #    Si 'sku_prefix' no viene, usamos el nombre real del lote
                prefix = sku_prefix or (lot_id.name if lot_id else '')
                if not prefix:
                    # Si ni x_sku_prefix ni lot_id está definido,
                    # podríamos omitir la generación de SKU o manejar otra lógica.
                    continue

                # f) Contador local para correlativo
                if prefix not in line_counter:
                    line_counter[prefix] = 1
                else:
                    line_counter[prefix] += 1

                # g) Generar SKU final y asignarlo
                sku = f"{prefix}-{str(line_counter[prefix]).zfill(3)}"
                move_line.sku_unico = sku

        return res
