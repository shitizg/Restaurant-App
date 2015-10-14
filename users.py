import web
from db import db
import bcrypt
from web import form
from web_render import render_page, render

class user_info:
    def GET(self):
        form = render.pwdchange('/user/info')
        return render_page(form)

    def POST(self):
        info = web.input()
        message = None
        uid = web.config._session.userid
        pword = str(info.old)
        upass = str(db.select('Users', vars=locals(),where='id=$uid', what='password')[0].password)
        if (info.new != info.repeated):
            message = "Passwords do not match"
        elif (upass == bcrypt.hashpw(pword, upass)):
            change_pass(uid, info.new)
            message = "Password updated successfully"
        else:
            message = "Invalid Password"

        form = render.pwdchange('/user/info', message=message)
        return render_page(form)

def add_user(uname, utype, passwd):
    db.insert('Users', uname=uname, role=utype,
            password=bcrypt.hashpw(str(passwd), bcrypt.gensalt()) )

def modify_user(uname, utype):
    db.update('Users', vars=dict(uname=uname, utype = utype), where="uname=$uname", role = utype)

def del_user(uname):
    db.delete("Users", vars=dict(uname=uname), where="uname=$uname")

def change_pass(uid, passwd):
    db.update('Users',vars=locals(),  where="id = $uid",
            password=bcrypt.hashpw(str(passwd), bcrypt.gensalt()) )

def get_users():
    users = db.select("Users join Role on Users.role = Role.id", what = "uname, Role.name as utype")
    return users.list()
