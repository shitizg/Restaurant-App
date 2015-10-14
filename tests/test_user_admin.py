import unittest
from unittest.case import SkipTest
import users
import bcrypt
from db import db

# User database integration tests
class test_user_db(unittest.TestCase):

    def setUp(self):
        self.passwd = "$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146" 
        db.delete('Users', where='id > 0')

    def test_add_user(self):
        users.add_user('kevin', 1, 'password')
        ret = db.select('Users', where="uname='kevin'")
        user = ret[0]
        self.assertEquals(user.uname, 'kevin')
        self.assertEquals(user.role, 1)
        phash = str(user.password);
        expected = bcrypt.hashpw('password', phash)
        self.assertEquals(expected, phash)

    def test_delete_user(self):
        uid = db.insert('Users', uname='kevin', role=1, password=self.passwd)
        users.del_user('kevin')
        ret = db.select('Users', where="id=$uid", vars=locals())
        with self.assertRaises(IndexError):
            print ret[0]

    def test_change_pass(self):
        uid = db.insert('Users', uname='kevin', role=1, password=self.passwd)
        users.change_pass(uid, 'newpassword')
        ret = db.select('Users', where="uname='kevin'")
        user = ret[0]
        phash = str(user.password);
        expected = bcrypt.hashpw('newpassword', phash)
        self.assertEquals(expected, phash)

    def test_get_users(self):
        users.add_user('kevin', 1, 'password')
        users.add_user('Mike', 2, 'password')
        userlist = users.get_users()
        self.assertEquals(len(userlist), 2)
        unames = ['kevin', 'Mike']
        for u in userlist:
            self.assertIn(u.uname, unames)

from mock import patch, MagicMock

class test_user_pass_change_web(unittest.TestCase):
    def setUp(self):
        self.passwd = "$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146" 
        db.delete('Users', where='id > 0')
        self.uid = db.insert('Users', uname='kevin', role=1, password=self.passwd)
        self.uinfo = users.user_info()

    def tearDown(self):
        db.delete('Users', where='id=$uid', vars=dict(uid=self.uid))

    @patch('web.config')
    @patch('web.input')
    def test_successful(self, mock_input, config):
        config._session.userid = self.uid
        mock_struct = MagicMock()
        mock_input.return_value = mock_struct
        mock_struct.old = 'password'
        mock_struct.new = 'newpassword'
        mock_struct.repeated = 'newpassword'
        result =  self.uinfo.POST()
        ret = db.select('Users', where="id=$uid", vars=dict(uid=self.uid))
        user = ret[0]
        phash = str(user.password);
        expected = bcrypt.hashpw('newpassword', phash)
        self.assertEquals(expected, phash)

    @patch('web.config')
    @patch('web.input')
    def test_wrong_password(self,mock_input, config):
        config._session.userid = self.uid
        mock_struct = MagicMock()
        mock_input.return_value = mock_struct
        mock_struct.old = 'garbage'
        mock_struct.new = 'newpassword'
        mock_struct.repeated = 'newpassword'
        result =  self.uinfo.POST()
        ret = db.select('Users', where="id=$uid", vars=dict(uid=self.uid))
        user = ret[0]
        phash = str(user.password);
        expected = bcrypt.hashpw('password', phash)
        self.assertEquals(expected, phash)

    @patch('web.config')
    @patch('web.input')
    def test_passwords_do_not_match(self,mock_input, config):
        config._session.userid = self.uid
        mock_struct = MagicMock()
        mock_input.return_value = mock_struct
        mock_struct.old = 'password'
        mock_struct.new = 'newpassword'
        mock_struct.repeated = 'wrong'
        result =  self.uinfo.POST()
        ret = db.select('Users', where="id=$uid", vars=dict(uid=self.uid))
        user = ret[0]
        phash = str(user.password);
        expected = bcrypt.hashpw('password', phash)
        self.assertEquals(expected, phash)

from manager import manager

class test_user_adding(unittest.TestCase):
    def setUp(self):
        db.delete('Users', where='id > 0')
        self.input_mock = MagicMock()
        self.winput = patch('web.input')
        self.input_mock.uname = 'kevin'
        self.input_mock.utype = 1
        self.input_mock.pword = 'password'
        self.config_mock = MagicMock()
        self.config = patch('web.config', new=self.config_mock)
        self.config_mock._session.roleid = 1
        self.manager = manager()

    def test_get_page(self):
        with self.winput:
            with self.config:
                result = self.manager.GET()
                self.assertIsNotNone(result)

    def test_create_user(self):
        with self.winput as webdata:
            self.input_mock.action ='create'
            webdata.return_value = self.input_mock
            with self.config:
                with self.assertRaises(Exception):
                    self.manager.POST()
        ret = db.select('Users', where="uname='kevin'")
        user = ret[0]
        self.assertEquals(user.uname, 'kevin')
        self.assertEquals(user.role, 1)
        phash = str(user.password);
        expected = bcrypt.hashpw('password', phash)
        self.assertEquals(expected, phash)

    def test_delete_user(self):
        users.add_user('kevin', 1, 'password')
        with self.winput as webdata:
            self.input_mock.action ='delete'
            webdata.return_value = self.input_mock
            with self.config:
                with self.assertRaises(Exception):
                    self.manager.POST()
        ret = db.select('Users', where="uname='kevin'")
        with self.assertRaises(IndexError):
            user = ret[0]
