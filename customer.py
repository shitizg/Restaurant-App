import web
import menu
from orders import add_item, delete_item, get_order, update_quantity
from web_render import render, render_page
from db import db

class customer_menu:
    def POST(self):
        #if (web.config._session.roleid != 4):
        #        raise web.seeother('/')
        pdata = web.input(item=None, order_id=None, action=None)
        if pdata.action == "order":
		add_item(pdata.order_id, pdata.item, 1)
        elif pdata.action == "remove":
                delete_item(pdata.order_id, pdata.item)
        orlist = get_order(pdata.order_id)
        tags = db.select('Categories').list()
        items = menu.get_menu_items()
        page = render.customer_banner(items, pdata.order_id, orlist, tags)
        return render_page(page)

class categories:
    def POST(self):
        data = web.input(category=None, order_id=None)
        orlist = get_order(data.order_id)
        items = menu.get_menu_items_category(data.category)
        tags = db.select('Categories').list()
        page = render.customer_banner(items, data.order_id, orlist, tags)
        return render_page(page)

class update_qty:
    def POST(self):
        item = web.input(item_id=None, order_id=None, qty=None)
        update_quantity(item.order_id, item.item_id, item.qty)
        orlist = get_order(item.order_id)
        items = menu.get_menu_items()
        tags = db.select('Categories').list()
        page = render.customer_banner(items, item.order_id, orlist, tags)
        return render_page(page)

