import web
from  web_render import render,render_page
from db import db

class complaint():

    # submit a new complaint to the system
    def POST(self):
        data = web.input(complaint=None, order_id=None)
        self.post_complaint(data.complaint, order=data.order_id)
        raise web.seeother('/customer_login?order_id='+data.order_id)

    # Shose complaints for waiter, or all for manager
    def GET(self):
        if web.config._session.roleid == 1 or web.config._session.roleid == 3:
            cplist = self.get_complaints()
        elif web.config._session.roleid == 2:
            cplist = self.get_complaints(waiter_id=web.config._session.userid)
        else:
            raise web.seeother('/')
        cpage = render.complaints(cplist)
        return render_page(cpage)

    def get_complaints(self, waiter_id=None):
        if waiter_id:
            results = db.select('Complaints', where="waiter_id="+str(waiter_id))
        else:
            results = db.select('Complaints')
        return results.list()

    def post_complaint(self, complaint, order=None):
        wid = None
        if order:
            od = db.select('Orders', what='waiter', where='id='+order)
            wid = od[0].waiter
        db.insert('Complaints', waiter_id=wid, complaint=complaint)
