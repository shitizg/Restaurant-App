#!/usr/bin/python2
import web

from orders import new_order, ret_order, new_item, new_quantity, move_to_top
from customer import customer_menu, update_qty, categories
from receipt import receipt, pay
from login import login, logout, customer_login
from alert import alert
from index import index
from manager import manager
from menu import menu, create_category, delete_category
from assistant import active_orders, complete_order, kitchen_status
from users import user_info
from web import form
from complaint import complaint

web.config.debug = False

urls = (
        '/', 'index',
        '/login', 'login',
        '/logout', 'logout',
	'/customer_login', 'customer_login',
	'/new_order', 'new_order',
	'/ret_order', 'ret_order',
	'/new_item', 'new_item',
	'/new_quantity','new_quantity',
	'/move_to_top', 'move_to_top',
        '/manager', 'manager',
        '/menu_editor', 'menu',
	'/customer_menu', 'customer_menu',
        '/user/info', 'user_info',
        '/complete_order', 'complete_order',
        '/active_orders', 'active_orders',
        '/complaint', 'complaint',
        '/kitchen_status', 'kitchen_status',
        '/update_qty', 'update_qty',
	'/alert', 'alert',
	'/receipt', 'receipt',
	'/pay', 'pay',
        '/complaints', 'complaint',
        '/categories', 'categories',
        '/create_category', 'create_category',
        '/delete_category', 'delete_category'
        )
app = web.application(urls, globals())
web.config._session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'loggedin' : False, 'role': "Login", 'roleid': 0})

if __name__ == "__main__":
    app.run()
