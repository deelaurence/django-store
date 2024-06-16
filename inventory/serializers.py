from rest_framework import serializers
from .models import InventoryItem, Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    suppliers = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Supplier.objects.all()
    )

    class Meta:
        model = InventoryItem
        fields = '__all__'

    def create(self, validated_data):
        suppliers_data = validated_data.pop('suppliers')
        inventory_item = InventoryItem.objects.create(**validated_data)
        for supplier_name in suppliers_data:
            supplier = Supplier.objects.get(name=supplier_name)
            inventory_item.suppliers.add(supplier)
        return inventory_item
