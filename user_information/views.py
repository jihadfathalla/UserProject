from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer , StausSerializer
import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from .models import CustomUser , Status





# Create your views here.






## task 1
@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def create_user(request):
     '''
          create user
          :params:request
          :return: success:201 created
     '''
     if request.method == 'POST':
          user_serialezer = UserSerializer(data=request.data,context={'user': request.user})
          if user_serialezer.is_valid():
               user_serialezer.save()
               data = {"data": user_serialezer.data}
               return Response(data['data'], status=status.HTTP_201_CREATED)
          else:
               data = {"error": user_serialezer.errors}
               return Response(data, status=status.HTTP_400_BAD_REQUEST)






## task 3
@api_view(['POST', ])
def create_status(request,phone_number,auth_token,status):
     '''
          create status
          :params:request
          :return: success:201 created
     '''
     try:
          user = CustomUser.objects.get(phone_number=phone_number)
          data = {'token': auth_token}
          try:
               valid_data = VerifyJSONWebTokenSerializer().validate(data)
               user = valid_data['user']
               staus_obj = Status(
                    user = user,
                    status = status
               )
               staus_obj.save()
               status_serialezer = StausSerializer(data=request.data)
               data = {"data": status_serialezer.data}
               return Response(data['data'], status=status.HTTP_201_CREATED)
          except CustomUser.DoesNotExist:
               data = {"error": "no user with this "}
               return Response(data, status=status.HTTP_400_BAD_REQUEST)
     except CustomUser.DoesNotExist:
          data = {"error": "no user with this credentials "}
          return Response(data, status=status.HTTP_401_Unauthorized)
    
          


    