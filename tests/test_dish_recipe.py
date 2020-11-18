# This file is part of tryton-corseg module. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.exceptions import UserError
from decimal import Decimal


class DishRecipeProductTestCase(ModuleTestCase):
    'Test Dish Recipe Product module'
    module = 'dish_recipe_product'

    @with_transaction()
    def test_product(self):
        pool = Pool()
        Recipe = pool.get('dish_recipe.recipe')
        Category = pool.get('dish_recipe.category')
        transaction = Transaction()

        category = Category(name='Category')

        product_1, unit = self._create_product('product_1', 'Unit')
        recipe = Recipe(
            name='Recipe',
            category=category,
            product=product_1,
            quantity=1.0,
            unit=unit,
        )
        recipe.save()
        self.assertEqual(recipe.rec_name, 'Recipe')

        # Do not allow to use a product that already belongs to a recipe
        self.assertRaises(UserError, Recipe.create, [{
                'product': product_1.id,
                }]
            )
        transaction.rollback()

    @classmethod
    def _create_product(cls, name, uom_name, service=False):
        pool = Pool()
        Template = pool.get('product.template')
        Product = pool.get('product.product')
        uom = cls._get_uom(uom_name)

        type_ = 'goods'
        if service:
            type_ = 'service'

        template=Template(
            name=name,
            default_uom=uom,
            type=type_,)
        template.save()

        product = Product(
            template=template
        )
        product.save()
        return product, uom

    @classmethod
    def _get_uom(cls, name):
        Uom = Pool().get('product.uom')
        # Kilogram, Gram, Unit
        uom = Uom.search([('name', '=', name)])[0]
        return uom


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        DishRecipeProductTestCase))
    return suite

