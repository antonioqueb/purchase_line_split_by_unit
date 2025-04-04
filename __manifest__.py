{
    'name': 'Purchase Line Split by Unit',
    'version': '1.1',
    'summary': 'Divide líneas por unidad y genera SKU único basado en lote',
    'description': '''
Divide automáticamente líneas de orden de compra por unidad si el producto usa tracking por lote.
Permite definir lote y prefijo SKU, y genera un campo SKU único por unidad al validar la recepción.
    ''',
    'author': 'Alphaqueb Consulting',
    'website': 'https://alphaqueb.com',
    'category': 'Purchases',
    'depends': ['purchase', 'stock'],
    'data': [
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
