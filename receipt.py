import web
from db import db
from orders import get_order
import waiter
from assistant import update_status
import menu
from web_render import render, render_page

class receipt:
    def POST(self):
        pdata = web.input(order_id = 0)
        rec_message = make_receipt(pdata.order_id)
        return waiter.make_waiter_page(message = rec_message)

    def GET(self):
        pdata = web.input(order_id = 0)
        return print_receipt(int(pdata.order_id))

class pay:
    def POST(self):
        pdata = web.input(order_id=0, action=None)
        session = web.config._session
        if(session.roleid == 2):
            mess = ""
            if str(pdata.action) == "accept":
                accept_receipt(int(pdata.order_id))
                mess = update_status(int(pdata.order_id), status=1)
            else:
                mess = reject_receipt(int(pdata.order_id))
            return waiter.make_waiter_page(message = mess)
        else:
            pay_receipt(int(pdata.order_id))
            return print_receipt(int(pdata.order_id))

def print_receipt(order_no):
    orlist = get_order(order_no)
    receipt = get_receipt(order_no)
    page = render.receipt(order_no, orlist, receipt)
    return render_page(page)

def get_receipt(order_no):
    args = dict(order_no=order_no)
    rec = db.select("Receipts", vars=args, where="order_id=$order_no").list()
    if len(rec) == 0:
        rec = db.select("Receipts", vars=args, where="id=0").list()
    return rec[0]

def delete_receipt(order_no):
    args = dict(order_no=order_no)
    db.delete("Receipts", vars=args, where="order_id=$order_no")

def add_receipt(order_no, total_price):
    args = dict(order_no=order_no)
    db.insert("Receipts", order_id=order_no, total=total_price)

def pay_receipt(order_no):
    args = dict(order_no=order_no)
    db.update("Receipts", vars=args, where="order_id=$order_no", paid=1)

def accept_receipt(order_no):
    args = dict(order_no=order_no)
    db.update("Receipts", vars=args, where="order_id=$order_no", paid=2)
    return "Receipt for order "+str(order_no)+" accepted"

def reject_receipt(order_no):
    args = dict(order_no=order_no)
    db.update("Receipts", vars=args, where="order_id=$order_no", paid=0)
    return "Receipt for order "+str(order_no)+" rejected"

def make_receipt(order_no):
    args = dict(order_no=order_no)
    if get_receipt(order_no).order_id == int(order_no):
        delete_receipt(order_no)
    rec_message = "Receipt for Order "+str(order_no)+" has been generated."

    items = get_order(order_no)
    total_price = 0
    for i in items:
        if isinstance(i.qty, int):
            total_price += i.price*int(i.qty)
    total_price = 1.1*total_price

    add_receipt(order_no, total_price)

    return rec_message
