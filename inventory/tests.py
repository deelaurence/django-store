from rest_framework.test import APITestCase
from rest_framework import status
from .models import InventoryItem, Supplier

class InventoryAPITestCase(APITestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name='Test Supplier', contact_info='Test Contact')
        self.inventory_item = InventoryItem.objects.create(name='Test Item', description='Test Description', price='10.00')
        self.inventory_item.suppliers.add(self.supplier)
    
    # InventoryItem Tests
    def test_create_inventory_item(self):
        response = self.client.post('/api/inventory/', {
            'name': 'New Item',
            'description': 'New Description',
            'price': '20.00',
            'suppliers': ['Test Supplier']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_inventory_item(self):
        response = self.client.put(f'/api/inventory/{self.inventory_item.id}/', {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'price': '15.00',
            'suppliers': ['Test Supplier']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory_item.refresh_from_db()
        self.assertEqual(self.inventory_item.name, 'Updated Item')

    def test_delete_inventory_item(self):
        response = self.client.delete(f'/api/inventory/{self.inventory_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InventoryItem.objects.filter(id=self.inventory_item.id).exists())

    # Supplier Tests
    def test_create_supplier(self):
        response = self.client.post('/api/suppliers/', {
            'name': 'New Supplier',
            'contact_info': 'New Contact'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_supplier(self):
        response = self.client.get(f'/api/suppliers/{self.supplier.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.supplier.name)

    def test_update_supplier(self):
        response = self.client.put(f'/api/suppliers/{self.supplier.id}/', {
            'name': 'Updated Supplier',
            'contact_info': 'Updated Contact'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Updated Supplier')

    def test_delete_supplier(self):
        response = self.client.delete(f'/api/suppliers/{self.supplier.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Supplier.objects.filter(id=self.supplier.id).exists())

    