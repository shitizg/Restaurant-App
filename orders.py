import web
from db import db
from web_render import render, render_page
import menu
import waiter

class new_order:
	def POST(self):
		waiter_id = web.config._session.userid
		order = create_new_order(waiter_id)
		return waiter.make_waiter_page(message = "Order: "+str(order)+" has been created.")

class ret_order:
	def GET(self):
		order = web.input(order_id = 0)
		orlist = get_order(order.order_id)
		rec = get_receipt(order.order_id)
		page = render.waiter_order_banner(order_id = order.order_id, olist = orlist, receipt = rec)
		return render_page(page)

class new_item:
	def POST(self):
		item = web.input(name=None, order_no=None, quantity=None)
		add_item(int(item.order_no), item.id, int(item.quantity))
		return waiter.make_waiter_page(message = "Item successfully added to order "+item.order_no)

class new_quantity:
	def POST(self):
		item = web.input(name=None, order_no=None, quantity=None)
		update_quantity(int(item.order_no), item.name, int(item.quantity))
		return waiter.make_waiter_page(message = item.quantity+" of Item: "+item.name+" added to order "+item.order_no)

class move_to_top:
	def POST(self):
		pdata = web.input(order_id=None, item_id = None, qty = None)
		delete_item(int(pdata.order_id), int(pdata.item_id))
		add_item(int(pdata.order_id), int(pdata.item_id), int(pdata.qty))
		orlist = get_order(pdata.order_id)
		rec = get_receipt(int(pdata.order_id))
		page = render.waiter_order_banner(order_id = pdata.order_id, olist = orlist, receipt = rec)
		return render_page(page)
		
def create_new_order(waiter_id):
    args = dict(waiter_id = waiter_id)
    #if (web.config._session.roleid != 2):
    #    raise Exception("Invalid role")
    order_id = db.insert("Orders", waiter=waiter_id)
    return order_id

def add_item(order, item, qty):
    res = db.insert("OrderedItems", order_id=order, item_id=item, qty = qty)

def update_quantity(order, item, qty):
    args = dict(order=order, item=item, qty=qty)
    res = db.update("OrderedItems", vars=args,
            where='order_id = $order and item_id = $item', qty = qty)

def delete_item(order, item):
    args = dict(order=order, item=item)
    db.delete("OrderedItems", vars=args, where='order_id = $order and item_id = $item')

def get_order(order):
    args = dict(order=order)
    result = db.select("OrderedItems join MenuItems", vars=args,
            where="order_id=$order and OrderedItems.item_id = MenuItems.id",
            order="position DESC")
    return result.list()

def get_receipt(order_no):
    args = dict(order_no=order_no)
    rec = db.select("Receipts", vars=args, where="order_id=$order_no").list()
    print (rec)
    if len(rec) == 0:
        rec = db.select("Receipts", vars=args, where="id=0").list()
    return rec[0]
