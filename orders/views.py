from rest_framework.response import Response
from .serializers import OrderItemSerializer,OrderSerializer
from .models import Order,OrderItem
from rest_framework.decorators import api_view,permission_classes
from accounts.permissions import IsCustomer,IsManager,IsDeliveryCrew
from cart.models import Cart
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User,Group
# Create your views here.
@api_view(['POST'])
@permission_classes([IsCustomer])
def place_order(request):
    try:
        cart=Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response({
            "message":"Cart is Empty"
        },status=status.HTTP_400_BAD_REQUEST)
    cart_items=cart.items.all()
    if not cart_items.exists():
        return Response({
            "message":"Cart is Empty"
        },status=status.HTTP_400_BAD_REQUEST)
    with transaction.atomic():
        order=Order.objects.create(user=request.user)
        total=Decimal('0.00')
        for cart_item in cart_items:
            item=cart_item.menuitem
            OrderItem.objects.create(order=order,menuitems=item,quantity=cart_item.quantity,unit_price=item.price)
            total+=item.price*cart_item.quantity
        order.total=total
        order.save()
        cart_items.delete()
        serializer=OrderSerializer(order)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
@api_view(['GET'])
@permission_classes([IsCustomer])
def my_orders(request):
    orders=Order.objects.filter(user=request.user).order_by('-date')
    serilaizer=OrderSerializer(orders,many=True)
    return Response(serilaizer.data)

@api_view(['PATCH'])
@permission_classes([IsManager])
def assign_orders(request,pk):
    delivery_crew_id=request.data.get('delivery_crew_id')
    try:
        order=Order.objects.get(pk=pk)
    except Order.DoesNotExist():
        return Response({"message":"The order does not exist"},status=status.HTTP_404_NOT_FOUND)
    try:
        delivery_crew=User.objects.get(id=delivery_crew_id)
    except User.DoesNotExist():
        return Response({"message":"Delivery Crew not Found"},status=status.HTTP_404_NOT_FOUND)
    if not delivery_crew.groups.filter(name="Delivery Crew").exists():
        return Response({"message":"User is not a delivery crew"},status=status.HTTP_400_BAD_REQUEST)
    order.delivery_crew=delivery_crew
    order.save()
    serializer=OrderSerializer(order)
    return Response(serializer.data)        

@api_view(['GET'])
@permission_classes([IsDeliveryCrew])
def pending_orders(request):
    orders=Order.objects.filter(status="pending").order_by('-date')
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsDeliveryCrew])
def mark_delivered(request,pk):
    try:
        order=Order.objects.get(pk=pk)
    except Order.DoesNotExist():
        return Response({"message":"Order not found"},status=status.HTTP_404_NOT_FOUND)
    order.status="delivered"
    order.save()
    serializer=OrderSerializer(order)
    return Response(serializer.data)