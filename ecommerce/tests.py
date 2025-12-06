from django.test import TestCase
from rest_framework.test import APIClient
from .models import Tenant, User, Product, Order, Customer
from django.urls import reverse

class EcommerceTestCase(TestCase):
    def setUp(self):
        # Create tenants
        self.tenant1 = Tenant.objects.create(store_name="Store A", contact_email="a@store.com", domain="storea.com")
        self.tenant2 = Tenant.objects.create(store_name="Store B", contact_email="b@store.com", domain="storeb.com")

        # Create users
        self.owner1 = User.objects.create_user(username="owner1", password="pass1234", role="owner", tenant=self.tenant1)
        self.staff1 = User.objects.create_user(username="staff1", password="pass1234", role="staff", tenant=self.tenant1)
        self.customer1 = User.objects.create_user(username="customer1", password="pass1234", role="customer", tenant=self.tenant1)

        # Create products
        self.product1 = Product.objects.create(name="Product1", price=100, stock=10, tenant=self.tenant1)
        self.product2 = Product.objects.create(name="Product2", price=200, stock=5, tenant=self.tenant2)

        # API Client
        self.client = APIClient()

    # -----------------------
    def test_tenant_product_isolation(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(reverse('product-list'))
        products = response.data
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['name'], "Product1")

    def test_jwt_token_claims(self):
        response = self.client.post(reverse('token_obtain_pair'), {"username": "owner1", "password": "pass1234"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_owner_permission(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.post(reverse('product-list'), {"name":"NewProd","price":50,"stock":20})
        self.assertEqual(response.status_code, 201)

    def test_staff_tenant_restriction(self):
        self.client.force_authenticate(user=self.staff1)
        response = self.client.get(reverse('product-detail', args=[self.product2.id]))
        self.assertEqual(response.status_code, 404)

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(user=self.customer1)
        response = self.client.post(reverse('product-list'), {"name":"CustProd","price":10,"stock":5})
        self.assertEqual(response.status_code, 403)
