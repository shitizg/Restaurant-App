import unittest
from orders import new_order, new_item, new_quantity
import orders
from db import db
from mock import MagicMock, patch

# DB Integration tests
class test_orders(unittest.TestCase):
    def setUp(self):
        db.delete('Orders', where='1=1')
        db.delete('OrderedItems', where='1=1')
        db.delete("MenuItems", where='1=1')
        db.insert('MenuItems', id=1, name='Chicken', description='Chicken', price=20)
        self.torders = new_order()
	self.titems = new_item()
	self.tquant = new_quantity()
        self.config_mock = MagicMock()
        self.config = patch('web.config', new=self.config_mock)
        self.config_mock._session.roleid = 2

    def test_create_order(self):
        with self.config:
            oi = orders.create_new_order(6)
        ret = db.select('Orders', where='id='+str(oi))
        to = ret[0]
        self.assertEquals(to.waiter, 6)
        self.assertEquals(to.status, 0)

    def test_add_item(self):
        with self.config:
            oi = orders.create_new_order(2)
	orders.add_item(oi, 1, 1)
        ret = db.select('OrderedItems', where='order_id='+str(oi))
        ti = ret[0]
        self.assertEquals(ti.item_id, 1)
