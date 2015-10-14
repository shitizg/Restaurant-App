import web
import os
from db import db
from web_render import render, render_page

class menu:
    def GET(self):
        if (web.config._session.roleid != 1):
            raise web.seeother('/')
        items = get_menu_items()
        tags = db.select('Categories').list()
        menu_table = render.menu_editor(items, tags)

        return render_page(menu_table)

    def POST(self):
        if (web.config._session.roleid != 1):
            raise web.seeother('/')
        pdata = web.input(item=None, action=None, picture={}, category_id=None)
        if pdata.action == "create":
            fullpath=None
            if 'picture' in pdata:#what I added for storing the picture
                if len(pdata.picture.filename)>0:
                    filedir='./static'
                    filepath=pdata.picture.filename.replace('\\','/')
                    filename=filepath.split('/')[-1]
		    fullpath=filedir+'/'+filename
                    fout=open(fullpath,'wb')
                    fout.write(pdata.picture.file.read())
                    fout.close()
            create_item(pdata.item, pdata.description, pdata.price,fullpath)
        elif pdata.action == 'delete':
            if len(pdata.picture)>0:
                os.remove(pdata.picture)
            delete_item(pdata.item)
        elif pdata.action == 'hide':
            set_status(pdata.item, False)
        elif pdata.action == 'show':
            set_status(pdata.item, True)
        elif pdata.action == 'update':
            db.update('MenuItems', where='id=$pdata.item', vars=locals(), price=pdata.price)
        elif pdata.action == 'category':
            db.insert('Item_Categories', item_id = pdata.item, category_id = pdata.category_id)
        elif pdata.action == 'delete_category':
            db.delete('Item_Categories', vars=locals(), where= 'item_id = $pdata.item and category_id = $pdata.category_id')
        raise web.seeother('/menu_editor')

class create_category:
    def POST(self):
        if (web.config._session.roleid != 1):
            raise web.seeother('/')
        pdata = web.input(category=None)
        db.insert('Categories', category = pdata.category)
        items = get_menu_items()
        tags = db.select('Categories').list()
        menu_table = render.menu_editor(items, tags)
        return render_page(menu_table)

class delete_category:
    def POST(self):
        pdata = web.input(category_id=None)
        print pdata.category_id
        db.delete('Categories', vars=locals(), where="id = $pdata.category_id")
        items = get_menu_items()
        tags = db.select('Categories').list()
        menu_table = render.menu_editor(items, tags)
        return render_page(menu_table)

def get_menu_items():
    menu_items = db.select('MenuItems')
    return menu_items.list()

def get_menu_items_category(category):
    item_list = db.select('MenuItems JOIN Item_Categories on id = item_id', vars = dict(category = category), where="category_id = $category").list()
    return item_list

def create_item( item, desc, price, picPath=None):
    db.insert('MenuItems', name=item, description=desc, price=price, picture=picPath)

def delete_item( item_id):
    db.delete('MenuItems', vars=locals(), where="id=$item_id")

def set_status( item_id, status):
    db.update('MenuItems', vars=locals(), where='id=$item_id', available=status)
