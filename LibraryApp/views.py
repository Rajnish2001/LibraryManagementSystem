from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from LibraryApp.models import Register
from LibraryApp.serializers import LibraryUserSerializer
import jwt, datetime

# Create your views here.
class LibraryUserRegister(APIView):
    def post(self, request):
        serializer = LibraryUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'User Registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LibraryUserLogin(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Register.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
        
        if type is None:
            raise AuthenticationFailed('Please Add User Type Field')

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'msg': user.usertype +' '+ 'Login Success' +' '+ user.name,
            'jwt':token
        }
        # serializer = LibraryUserSerializer(user)

        # return Response(serializer.data)
        return response


class LibraryUserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated!')

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = Register.objects.filter(id=payload['id']).first()
        serializer = LibraryUserSerializer(user)
        return Response(serializer.data)

class LibraryUserLogoutView(APIView):  
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'msg':'Success'
        }
        return response


