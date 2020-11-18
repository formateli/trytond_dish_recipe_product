#This file is part of tryton-dish_recipe project. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Bool, Eval, If
from trytond.exceptions import UserError
from trytond.i18n import gettext

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

    @classmethod
    def __setup__(cls):
        super(Recipe, cls).__setup__()
        cls.components.domain.append(
                ('product', '!=', Eval('product')),
            )
        cls.components.depends += ['product']

    @fields.depends('unit')
    def on_change_with_unit_digits(self, name=None):
        if self.unit:
            return self.unit.digits
        return 2

    @fields.depends('product')
    def on_change_with_product_uom_category(self, name=None):
        if self.product:
            return self.product.default_uom_category.id

    @classmethod
    def validate(cls, recipes):
        for recipe in recipes:
            if recipe.product:
                rcp = cls.search([
                        ('product', '=', recipe.product.id),
                        ('id', '!=', recipe.id),
                    ])
                if rcp:
                    raise UserError(
                        gettext('dish_recipe_product.msg_product_selected',
                            product=product.rec_name,
                            recipe=recipe.rec_name,
                            rcp=rcp.rec_name))
        super(Recipe, cls).validate(recipes)
