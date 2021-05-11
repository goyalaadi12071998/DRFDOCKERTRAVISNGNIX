from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from django.db.models import Q
import datetime
import jwt

@api_view(['POST'])
def register_user(request):
    
    name = request.data['name']
    email = request.data['email']
    phone = request.data['phone']
    password = request.data['password']

    try:
        existinguser = User.objects.filter(Q(name=name) | Q(phone=phone))
        if existinguser:
            return Response({"msg":"User already exists"},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(name=name, email=email, phone=phone, password=password)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except ValueError as err:
        print(type(err))
        print(str(err.args))
        return Response({"msg":str(err.args)},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    
    email = request.data['email']
    password = request.data['password']
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        raise AuthenticationFailed("User email not found")

    if not user.check_password(password):
        raise AuthenticationFailed("Password is incorrect")
    
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload,'secret',algorithm='HS256')
    
    serializer = UserSerializer(user)
    response = Response(serializer.data,status=status.HTTP_200_OK)
    response.set_cookie(key='jwt', value=token, httponly=True)
    
    return response


@api_view(['GET'])
def user_detail(request):
    
    token = request.COOKIES['jwt']
    if not token:
        raise AuthenticationFailed("Unauthenticated")

    
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError as err:
        raise AuthenticationFailed("Unauthenticated")
    
    
    user = User.objects.get(id=payload['id'])
    serializer = UserSerializer(user)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def logout_user(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        "msg": "Logging out"
    }
    return response