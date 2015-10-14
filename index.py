import web
from web_render import render, render_page
import waiter


from menu import get_menu_items
class index():
    def GET(self):
        session = web.config._session
        if (session.roleid == 2):
            return waiter.make_waiter_page()
        elif (session.roleid == 1):
            raise web.seeother('/manager')
        elif (session.roleid == 3):
            raise web.seeother('/active_orders')
        elif (session.roleid == 4):
            raise web.seeother('/customer_login')

        return render_page(None)
