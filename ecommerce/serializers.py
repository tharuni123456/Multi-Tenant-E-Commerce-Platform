from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tenant, Product, Customer, Order, OrderItem

User = get_user_model()

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role", "tenant_id")

    def create(self, validated_data):
        pw = validated_data.pop("password")
        tenant_id = validated_data.pop("tenant_id", None)
        user = User(**validated_data)
        if tenant_id:
            from .models import Tenant
            user.tenant = Tenant.objects.get(id=tenant_id)
        user.set_password(pw)
        user.save()
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("tenant", "created_at")

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ("tenant",)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "price", "qty")
        read_only_fields = ("price",)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    class Meta:
        model = Order
        fields = ("id", "vendor", "tenant", "customer", "placed_by", "status", "total_amount", "items", "created_at")
        read_only_fields = ("tenant", "placed_by", "total_amount", "created_at")
    # NOTE: keep 'tenant' in signature for clarity but we don't expect clients to send it
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        tenant = self.context['request'].user.tenant
        order = Order.objects.create(tenant=tenant, placed_by=self.context['request'].user, **validated_data)
        total = 0
        for item in items_data:
            product = item["product"]
            price = product.price
            qty = item.get("qty", 1)
            OrderItem.objects.create(order=order, product=product, price=price, qty=qty)
            total += price * qty
        order.total_amount = total
        order.save()
        return order
