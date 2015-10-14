import web
import users
from orders import get_order
from db import db
from web_render import render_page, render

class active_orders:
    def GET(self):
            olist = db.select('Orders', where="status == 0").list()
            page = render.kitchen_banner(olist)
            return render_page(page)

class kitchen_status:
    def GET(self):
            olist = db.select('Orders', where="status == 0").list()
            olist2 = db.select('Orders', where="status == 1").list()
            page = render.kitchen_status(olist,olist2)
            return render_page(page)

class complete_order:
    def POST(self):
            order = web.input(order_id = 0)
            update_status(int(order.order_id), status=1)
            raise web.seeother('/active_orders')

class view_ingredients:
    def GET(self):
            names = db.select('Ingredient_Inventory', what="inredient").list()
            qtys = db.select('Ingredient_Inventory', what ="qty").list()
            page = render.inventory_banner(names, qtys)
            return render_page(page)
            qtys = db.select('Ingredient_Inventory', where="")

#def get_inventory_qty:

def update_status(order, status):
    args = dict(order = order)
    res = db.update('Orders', vars=args,
            where='id = $order', status = status)
    update_ingredients(order);

#def get_item_qty(item_id):
#    return db.select('Item_Ingredients join MenuItems', vars = dict(item_id = item_id), where='id = $item_id', what="qty").list()

def get_ingredients(item_id):
    return db.select('Item_Ingredients', vars = dict(item_id = item_id), where='id = $item_id').list()

def update_qty(ingredient, qty):
    init = db.select('Ingredient_Inventory', vars = dict(ingredient = ingredient), where='ingredient=$ingredient').list()
    args = dict(ingredient = ingredient)
    for x in init:
        res = db.update('Ingredient_Inventory', vars = args, where='ingredient = $ingredient', qty = x.qty - qty)

def update_ingredients(order):
    olist = get_order(order)
    print olist;
#   item_ids = db.select('OrderedItems join MenuItems', vars=args, where='order_id = $order').list()
    for item in olist:
        print item.item_id
        ingredients = get_ingredients(item.item_id)
        for ingredient in ingredients:
            update_qty(ingredient.ingredient, ingredient.qty)
