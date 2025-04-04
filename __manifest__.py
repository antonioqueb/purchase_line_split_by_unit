{
    'name': 'Purchase Line Split by Unit',
    'version': '1.1.1',
    'summary': 'Divide líneas de compra por unidad y genera SKU único por lote',
    'description': '''
Este módulo permite dividir automáticamente las líneas de orden de compra en unidades individuales
cuando el producto utiliza seguimiento por lote. También permite definir un lote común y un prefijo de SKU
en la orden de compra, los cuales se propagan a las líneas de recepción. Al validar la recepción, el sistema
genera un SKU único secuencial por cada unidad basada en el prefijo o nombre del lote.

Ideal para trazabilidad detallada sin necesidad de activar números de serie.
    ''',
    'author': 'Alphaqueb Consulting',
    'website': 'https://alphaqueb.com',
    'category': 'Purchases',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
        'stock',
    ],
    'data': [
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
