#This file is part of tryton-dish_recipe_product project. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import dish_recipe
from . import product


def register():
    Pool.register(
        dish_recipe.Recipe,
        product.Product,
        module='dish_recipe_product', type_='model')
