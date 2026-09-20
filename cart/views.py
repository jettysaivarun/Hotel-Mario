from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Cart,CartItem
from menu.models import MenuItem
from rest_framework import status
from .serializers import CartItemSerializer,CartSerializer
from accounts.permissions import IsCustomer
from rest_framework.response import Response
# Create your views here.

@api_view(['POST'])
@permission_classes([IsCustomer])
def add_to_cart(request):
    menuitem_id=request.data.get('menuitem')
    quantity=request.data.get('quantity')
    try:
        menu_item=MenuItem.objects.get(id=menuitem_id)
    except MenuItem.DoesNotExist:
        return Response({
            "message":"Item not found"
        },status=status.HTTP_404_NOT_FOUND)
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_item,created=CartItem.objects.get_or_create(cart=cart,menuitem=menu_item)
    
    if created:
        cart_item.quantity=quantity
    else:
        cart_item.quantity+=quantity
    cart_item.save()
    serializer=CartItemSerializer(cart_item)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsCustomer])
def view_cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    serializer=CartSerializer(cart)
    return Response(serializer.data)