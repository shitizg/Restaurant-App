import web
import menu
from orders import get_order
from web_render import render, render_page
from db import db

class alert:
	def POST(self):
		pdata = web.input(order_id=0)
		add_alert(pdata.order_id)
		orlist = get_order(pdata.order_id)
		items = menu.get_menu_items()
		tags = db.select('Categories').list()

		page = render.customer_banner(items, pdata.order_id, orlist, tags)
		return render_page(page)
		

def add_alert(order_id):
	db.insert('Alerts', order_id=int(order_id))
