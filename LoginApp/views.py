from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from . serializers import UserSerializer, UserSerializerWithToken, ProductSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.core import mail
from django.conf import settings
from django.views.generic import View


# Create your views here.

@api_view(['GET'])
def GetRoute(request):
    return Response('Hello Manasha')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v       
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


@api_view(['GET'])
def  GetUserProfile(request):
    user=request.user
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def GetUsers(request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def RegisterUser(request):
    data=request.data
    try:
        print(data)
        user= User.objects.create(first_name=data['fname'],last_name=data['lname'],username=data['email'],email=data['email'],password=make_password(data['password']), is_active=False)

        
        # token for email
        email_subject="Activate Your Account"
        message=render_to_string(
            "activate.html",
           {
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
           }

        )
        print(message)
        connection = mail.get_connection()
        connection.open()

        email_message=mail.EmailMessage(email_subject, message, settings.EMAIL_HOST_USER,[data['email']])
        email_message.send()
        message={'details':'Activate Your Account, Please check your email for the activation link.'}
        
        serialize=UserSerializerWithToken(user,many=False)
        return Response(serialize.data)

    except Exception as e:
        message = {'details': 'Email Address already exists'} 
        print(e)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as indentifier:
            user = None
        
        if user is not None and generate_token.check_token(user, token):
            user.is_active=True
            user.save()
            # message = {'details': 'Account is Activated!'}
            return render(request, "activatesuccess.html")
        
        else:
            return render(request, "activatefail.html")


@api_view(['GET'])
def GetProducts(self, request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def PostProduct(self, request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete(self, request, product_id):
    try:
        to_delete_product = Product.objects.get(product_id=product_id)
        if to_delete_product is not None:
            to_delete_product.delete()
            return Response(f'{product_id} deleted successfully')
    except Products.DoesNotExist:
        return Response(f'Product with ID {product_id} does not exist',status=status.HTTP_404_NOT_FOUND)
