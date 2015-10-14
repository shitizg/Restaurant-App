import web
import bcrypt
from db import db
import menu
from orders import add_item, delete_item, get_order
from web_render import render, render_page

class login:
    def POST(self):
        upass = web.input(username=None,password = None)
        user_data = self.login_user(upass.username.encode('UTF-8'), upass.password.encode('UTF-8'))
        if user_data == None:
            return render_page("Username or password not valid")
        web.config._session.loggedin = True
        web.config._session.role = user_data.user_type
        web.config._session.roleid = user_data.roleid
        web.config._session.userid = user_data.uid
        #return str(upass.username) + " logged in as " + user_type
        raise web.seeother('/')

    def login_user(self, user, password):
        user_data = self.get_user(user)
        if (user_data == None):
            return None
        elif (str(user_data.password) == bcrypt.hashpw(password, str(user_data.password))):
            return user_data
        else:
            return None

    def get_user(self,username):
        #user = User("manager", "$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146", "manager")
        users = db.select('Users join Role', dict(username=username),
                where="uname = $username and Users.role = Role.id",
                what='Users.id as uid,uname,password,Role.id as roleid, Role.name as user_type').list()
        if (len(users) == 1 ):
            return users[0]

class logout:
    def POST(self):
        web.config._session.loggedin = False
        web.config._session.role = "Login"
        web.config._session.roleid = 0
        web.config._session.userid = 0
        raise web.seeother('/')

class customer_login:
    def POST(self):
        pdata = web.input(order_id = None)
        orlist = get_order(pdata.order_id)
        items = menu.get_menu_items()
        tags = db.select('Categories').list()
        page = render.customer_banner(items, pdata.order_id, orlist, tags)
        return render_page(page)
    def GET(self):
        pdata = web.input(order_id = None)
        orlist = get_order(pdata.order_id)
        items = menu.get_menu_items()
        tags = db.select('Categories').list()
        page = render.customer_banner(items, pdata.order_id, orlist, tags)
        return render_page(page)
