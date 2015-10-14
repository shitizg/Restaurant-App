import web
import users
import menu
from web_render import render, render_page
from db import db

class manager:
    def GET(self):
        if (web.config._session.roleid != 1):
            raise web.seeother('/')
        userlist = users.get_users()
        utable = render.user_list(userlist)
        return render_page(utable)

    def POST(self):
        if (web.config._session.roleid != 1):
            raise web.seeother('/')
        pdata = web.input(uname=None, action=None)
        if pdata.action == "create":
            users.add_user(pdata.uname, pdata.utype, pdata.pword)
        elif pdata.action == "modify":
            users.modify_user(pdata.uname, pdata.utype)
        elif pdata.action == 'delete':
            users.del_user(pdata.uname)
        raise web.seeother('/manager')
