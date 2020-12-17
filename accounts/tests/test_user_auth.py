import unittest
from django.test import TestCase

from accounts.models import User


class TestUserAuth(TestCase):
    def test_user_is_empty(self):
        registered_user = User.objects.all()
        self.assertEqual(registered_user.count(), 0)

    def test_user_not_empty(self):
        user = User()
        user.save()
        registered_user = User.objects.all()
        self.assertEqual(registered_user.count(), 1)

    def test_user_detail(self):
        user = User()
        user.email = 'aaa@icloud.com'
        user.last_name = 'テスト'
        user.first_name = 'TEST'
        user.password = 'aaaaaa'
        user.address = 'Japan'
        user.tel = '08011112222'
        user.is_customer = True
        user.save()

        registered_user = User.objects.all()
        existed_user = registered_user[0]

        self.assertEqual(existed_user.email, 'aaa@icloud.com')
        self.assertEqual(existed_user.last_name, 'テスト')
        self.assertEqual(existed_user.first_name, 'TEST')
        self.assertEqual(existed_user.password, 'aaaaaa')
        self.assertEqual(existed_user.address, 'Japan')
        self.assertEqual(existed_user.tel, '08011112222')
        self.assertEqual(existed_user.is_customer, True)
        self.assertEqual(registered_user.count(), 1)
