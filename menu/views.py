from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
# Create your views here.

from .models import Category,MenuItem
from .serializers import CategorySerializer,MenuItemSerializer
from accounts.permissions import IsManager

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories(request):
    category=Category.objects.all()
    serializer=CategorySerializer(category,many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    items=MenuItem.objects.all()
    category=request.GET.get('category')
    if category:
        items=items.filter(category_id=category)
    ordering=request.GET.get('ordering')
    if ordering=="price":
        items=items.order_by('price')
    elif ordering=="-price":
        items=items.order_by('-price')
    paginator=PageNumberPagination()
    paginator.page_size=3
    result_page=paginator.paginate_queryset(items,request)      
    serializer=MenuItemSerializer(items,many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsManager])
def update_item_of_the_day(request,pk):
    try:
        item=MenuItem.objects.get(id=pk)
    except MenuItem.DoesNotExist:
        return Response({
            "message":"Item not found",
        },status=status.HTTP_404_NOT_FOUND)
    
    featured=request.data.get("featured")
    if featured is True:
        MenuItem.objects.exclude(id=pk).update(featured=False)
    item.featured=featured
    item.save()
    serializer=MenuItemSerializer(item)
    
    return Response(serializer.data)
