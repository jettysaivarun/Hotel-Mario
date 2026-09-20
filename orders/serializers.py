from rest_framework import serializers
from .models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=["id","menuitems","quantity","unit_price"]

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=[
            'id',
            'user',
            'delivery_crew',
            'status',
            'total',
            'date',
            'items'
            ]