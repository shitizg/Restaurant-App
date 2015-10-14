import unittest
from mock import MagicMock, patch
from login import login

class login_test(unittest.TestCase):
    def setUp(self):
        self.loginclass = login()
        self.patcher = patch('login.login.get_user')
        self.mock = self.patcher.start()
        user = MagicMock()
        user.uname = "manager"
        user.password = "$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146"
        user.user_type = "manager"
        self.mock.return_value = user

    def tearDown(self):
        patch.stopall()

    def test_correct_type_on_login(self):
        user = self.loginclass.login_user("manager", "password")
        utype = user.user_type
        self.assertEqual(utype, "manager")

    @patch('login.login.get_user')
    def test_unsuccessful_login(self, mock_get_user):
        mock_get_user.return_value = None
        utype = self.loginclass.login_user("manager", "password")
        self.assertEqual(utype, None)

    def test_wrong_password_fails(self):
        utype = self.loginclass.login_user("manager", "wrongpassword")
        self.assertEqual(utype, None)

from login import logout
from mock import MagicMock, patch
from db import db

class login_test_web(unittest.TestCase):
    def setUp(self):
        self.passwd = "$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146" 
        db.delete('Users', where='id > 0')
        self.uid = db.insert('Users', uname='kevin', role=1, password=self.passwd)
        self.input_mock = MagicMock()
        self.winput = patch('web.input')
        self.config_mock = MagicMock()
        self.config = patch('web.config', new=self.config_mock)
        self.login_web = login()
        self.logout_web = logout()

    def test_get_user(self):
        user = self.login_web.get_user('kevin')
        self.assertEquals(user.roleid, 1)
        self.assertEquals(user.uname, 'kevin')
        self.assertEquals(user.password, self.passwd)
        self.assertEquals(user.uid, self.uid)
        self.assertEquals(user.user_type, 'Manager')

    def test_web_login_successful(self):
        with self.winput as webin:
            self.input_mock.username = 'kevin'
            self.input_mock.password = 'password'
            webin.return_value = self.input_mock
            with self.config as conf:
                with self.assertRaises(Exception):
                    self.login_web.POST()
                self.assertEquals(str(conf._session.role), 'Manager')
                self.assertEquals(conf._session.roleid, 1)
                self.assertEquals(conf._session.userid, self.uid)
                self.assertTrue(conf.loggedin)

    def test_web_login_fails(self):
        with self.winput as webin:
            self.input_mock.username = 'kevin'
            self.input_mock.password = 'garbage'
            webin.return_value = self.input_mock
            with self.config as conf:
                self.login_web.POST()
                self.assertNotEquals(str(conf._session.role), 'Manager')
                self.assertNotEquals(conf._session.roleid, 1)
                self.assertNotEquals(conf._session.userid, self.uid)
                self.assertNotEquals(conf._session.loggedin, True)

    def test_web_logout_unset(self):
        with self.winput as webin:
            webin.return_value = self.input_mock
            with self.config as conf:
                conf._session.loggedin = True
                conf._session.role = 'Manager'
                conf._session.roleid = 1
                conf._session.userid = self.uid
                with self.assertRaises(Exception):
                    self.logout_web.POST()
                self.assertEquals(str(conf._session.role), 'Login')
                self.assertEquals(conf._session.roleid, 0)
                self.assertEquals(conf._session.userid, 0)
                self.assertFalse(conf._session.loggedin)
