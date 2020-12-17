import unittest
from django.test import TestCase

from accounts.models import Supplier, User


class TestSupplierAuth(TestCase):
    def test_supplier_is_empty(self):
        registered_supplier = Supplier.objects.all()
        self.assertEqual(registered_supplier.count(), 0)

    def test_supplier_detail(self):
        test_user = User()
        test_user.email = 'email'
        test_user.last_name = 'last_name'
        test_user.first_name = 'first_name'
        test_user.password = 'password'
        test_user.address = 'Japan'
        test_user.tel = '08011112222'
        test_user.is_supplier = True
        test_user.save()

        supplier = Supplier()
        supplier.user = test_user
        supplier.company_name = 'ABC株式会社'
        supplier.save()

        registered_supplier = Supplier.objects.all()
        existed_supplier = registered_supplier[0]

        self.assertEqual(test_user.email, 'email')
        self.assertEqual(test_user.last_name, 'last_name')
        self.assertEqual(test_user.first_name, 'first_name')
        self.assertEqual(test_user.password, 'password')
        self.assertEqual(test_user.address, 'Japan')
        self.assertEqual(test_user.tel, '08011112222')
        self.assertEqual(existed_supplier.company_name, 'ABC株式会社')
        self.assertEqual(test_user.is_supplier, True)
        self.assertEqual(registered_supplier.count(), 1)