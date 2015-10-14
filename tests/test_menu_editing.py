import unittest
from menu import *
from db import db

# DB Integration tests
class test_menu_db(unittest.TestCase):
    def setUp(self):
        db.delete('MenuItems', where='1=1')
        self.menued = menu()

    def test_create_item(self):
        create_item('Chicken', 'Chicken Desc', 30)
        ret = db.select('MenuItems', where='name="Chicken"')
        mitem = ret[0]
        self.assertEquals(mitem.name, 'Chicken')
        self.assertEquals(mitem.description, 'Chicken Desc')
        self.assertEquals(mitem.price, 30.0)
        self.assertTrue(mitem.available)

    def test_delete_item(self):
        itemid = db.insert('MenuItems', name= 'Chicken', description='Desc',
                price=20)
        delete_item(itemid)
        ret = db.select('MenuItems', where='name="Chicken"')
        with self.assertRaises(IndexError):
            mitem = ret[0]

    def test_set_status(self):
        itemid = db.insert('MenuItems', name= 'Chicken', description='Desc',
                price=20)
        set_status(itemid, False)
        ret = db.select('MenuItems', where='name="Chicken"')
        mitem = ret[0]
        self.assertFalse(mitem.available)

    def test_get_menu_items(self):
        create_item('Chicken', 'Chicken Desc', 30)
        create_item('Pork', 'Pork Desc', 30)
        itemnames = ['Chicken', 'Pork']
        ret = get_menu_items()
        self.assertEquals(len(ret), 2)
        for item in ret:
            self.assertIn(item.name, itemnames)

from mock import MagicMock, patch

class test_web_menu(unittest.TestCase):
    def setUp(self):
        db.delete('MenuItems', where='1=1')
        self.input_mock = MagicMock()
        self.winput = patch('web.input')
        self.config_mock = MagicMock()
        self.config = patch('web.config', new=self.config_mock)
        self.config_mock._session.roleid = 1
        self.menued = menu()

    def test_web_get_menu(self):
        with self.winput:
            with self.config:
                result = self.menued.GET()
                self.assertIsNotNone(result)

    def test_web_create_item(self):
        with self.winput as info:
            self.input_mock.action = 'create'
            self.input_mock.item = "Chicken"
            self.input_mock.description = "Chicken Desc"
            self.input_mock.price = 30
            info.return_value = self.input_mock
            with self.config:
                with self.assertRaises(Exception):
                    self.menued.POST()
        ret = db.select('MenuItems', where='name="Chicken"')
        mitem = ret[0]
        self.assertEquals(mitem.name, 'Chicken')
        self.assertEquals(mitem.description, 'Chicken Desc')
        self.assertEquals(mitem.price, 30.0)
        self.assertTrue(mitem.available)

    def test_web_delete_item(self):
        itemid = db.insert('MenuItems', name= 'Chicken', description='Desc',
                price=20)
        with self.winput as info:
            self.input_mock.action = 'delete'
            self.input_mock.item = itemid
            info.return_value = self.input_mock
            with self.config:
                with self.assertRaises(Exception):
                    self.menued.POST()
        ret = db.select('MenuItems', where='1=1')
        with self.assertRaises(IndexError):
            mitem = ret[0]

    def test_web_hide_item(self):
        itemid = db.insert('MenuItems', name= 'Chicken', description='Desc',
                price=20)
        with self.winput as info:
            self.input_mock.action = 'hide'
            self.input_mock.item = itemid
            info.return_value = self.input_mock
            with self.config:
                with self.assertRaises(Exception):
                    self.menued.POST()
        ret = db.select('MenuItems', where='id=$itemid', vars=locals())
        mitem = ret[0]
        self.assertFalse(mitem.available)

    def test_web_show_item(self):
        itemid = db.insert('MenuItems', name= 'Chicken', description='Desc',
                price=20)
        set_status(itemid, False)
        with self.winput as info:
            self.input_mock.action = 'show'
            self.input_mock.item = itemid
            info.return_value = self.input_mock
            with self.config:
                with self.assertRaises(Exception):
                    self.menued.POST()
        ret = db.select('MenuItems', where='id=$itemid', vars=locals())
        mitem = ret[0]
        self.assertTrue(mitem.available)

    def test_web_update_item(self):
        itemid = db.insert('MenuItems', name= 'Chicken', description='Desc',
                price=20)
        with self.winput as info:
            self.input_mock.action = 'update'
            self.input_mock.item = itemid
            self.input_mock.price = 15
            info.return_value = self.input_mock
            with self.config:
                with self.assertRaises(Exception):
                    self.menued.POST()
        ret = db.select('MenuItems', where='id=$itemid', vars=locals())
        mitem = ret[0]
        self.assertEquals(mitem.price, 15)
