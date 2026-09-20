from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from .permissions import IsManager
from django.contrib.auth.models import User,Group
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_api(request):
    return Response(
        {
            "message":"Authentication Successful",
            "usename":request.user.username,
        }
    )

@api_view(['POST'])
def RegistrationView(request):
    serializer=RegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message":"User Registration Successful",
            
        },status=status.HTTP_201_CREATED)
    return Response({
        "message":"Try Again",
        "error":serializer.errors,
    },status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsManager])
def assign_orders_to_deliverycrew(request):
    user_id=request.data.get("user_id")
    try:
        user=User.objects.get(id=user_id)
    except User.DoesNotExist():
        return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
    
    group,created=Group.objects.get_or_create(name='Delivery Crew')
    user.groups.add(group)
    return Response({"message":f"{user.username} is assigned to the delivery crew"})