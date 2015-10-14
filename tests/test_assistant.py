import unittest
from mock import MagicMock, patch
from assistant import update_status
from db import db

#Integration Tests
class complete_order_test(unittest.TestCase):
    def setUp(self):
        self.oid = db.insert('Orders', waiter = 2)

    def tearDown(self):
        db.delete('Orders', vars=dict(oid=self.oid), where="id=$oid")

    def test_update_status(self):
        update_status(self.oid, 1)
        status = db.select('Orders', vars=dict(oid=self.oid), where='id=$oid', what='status')
        updStatus = status[0]
        self.assertEquals(updStatus.status, 1)

from mock import MagicMock, patch
from assistant import update_status
from db import db

class active_orders_test(unittest.TestCase):
    def setUp(self):
        self.olist = range(0,5)
        for x in xrange(0,5):
            self.olist[x] = db.insert('Orders', waiter = 2)

    def tearDown(self):
        for x in xrange(0,5):
            db.delete('Orders', vars=dict(oid=self.olist[x]), where="id=$oid")

    def test_active_order(self):
        for x in xrange(0,5):
            tmp = range(0,5)
            tmp = db.select('Orders', vars=dict(oid=self.olist[x]), where='id=$oid')
            self.assertEquals(tmp[0].id, self.olist[x])
