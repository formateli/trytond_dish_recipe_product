
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = [
        'Recipe',
    ]


class Recipe(metaclass=PoolMeta):
    __name__ = 'dish_recipe.recipe'

    product = fields.Many2One('product.product', 'Product associated',
        help='Product associated with this recipe.')
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')
    quantity = fields.Float('Quantity',
        digits=(16, Eval('unit_digits', 2)),
        states={
            'required': Bool(Eval('product')),
        },
        depends=['product', 'unit_digits'])
    unit = fields.Many2One('product.uom', 'Unit',
        domain=[
            If(Bool(Eval('product_uom_category')),
                ('category', '=', Eval('product_uom_category')),
                ('category', '=', -1)),
            ],
        states={
            'required': Bool(Eval('product')),
        },
        depends=['product', 'product_uom_category'])
    product_uom_category = fields.Function(
        fields.Many2One('product.uom.category', 'Product Uom Category'),
        'on_change_with_product_uom_category')

    @fields.depends('unit')
    def on_change_with_unit_digits(self, name=None):
        if self.unit:
            return self.unit.digits
        return 2

    @fields.depends('product')
    def on_change_with_product_uom_category(self, name=None):
        if self.product:
            return self.product.default_uom_category.id
