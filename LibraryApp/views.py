from heapq import merge
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from yaml import serialize
from LibraryApp.models import Register,Books,Student,Book_issues
from LibraryApp.serializers import LibraryUserSerializer,BookSerializer,StudenSerializer,BookIssueSerializer
import jwt, datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
import json,io
from rest_framework.parsers import JSONParser

# from LibraryManagementSystem.LibraryApp import serializers

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
        
        
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'msg': 'Librarian Login Success' +' '+ user.name,
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

    #For Adding Books
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')

        user = Register.objects.filter(id=payload['id']).first()
        if user is not None:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg':'Book Added'},status=status.HTTP_201_CREATED)

    # For Deleting Books
    def delete(self,request,pk=None):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')
        user = Register.objects.filter(id=payload['id']).first()
        if user is not None:
            query = Books.objects.get(id=pk)
            query.delete()
            return Response({'msg':query.title+' '+'Book is deleted'},status=status.HTTP_202_ACCEPTED)
    
#Books filter is pending
class BooksView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')
        user = Register.objects.filter(id=payload['id']).first()
        if user is not None:
            book = Books.objects.all
            serialize = BookSerializer(book,many=True)
            filter_backends = [DjangoFilterBackend,SearchFilter]
            filterset_fields = ['title']
            search_fields = ['title']
            # def get_queryset(self):
            #     books = self.request.title #Stored Current user value
            #     print('======',books)
            #     return Student.objects.filter(title = books)
            return Response(serialize.data)

# Book issue for student
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('User Unauthenticated!, Please Login first.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User Unauthenticated!, Please Login first.')

        user = Register.objects.filter(id=payload['id']).first()

        data = request.data

        LibraryUser = user.id
        data["librarian"]=LibraryUser
        # print(data)

        serializer = BookIssueSerializer(data=data)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class LibraryUserLogoutView(APIView):  
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'msg':'Success'
        }
        return response














# class BooksView(APIView):
#     def post(self,request):
        
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':'Book added'},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StudentView(APIView):
    def post(self, request):
        serializer = StudenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Student Registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StudentLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Student.objects.get(email=email)

        if user is None:
            raise AuthenticationFailed('User Not Found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
        

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='stu', value=token, httponly=True)

        response.data = {
            'msg': 'Student Login Success' +' '+ user.name,
            'jwt':token
        }
        # serializer = LibraryUserSerializer(user)

        # return Response(serializer.data)
        return response


    def get(self,request):
        token = request.COOKIES.get('stu')
        if not token:
            raise AuthenticationFailed('unauthenticated!')

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = Student.objects.filter(id=payload['id']).first()
        usr = Book_issues.objects.filter(student=user).all()
        print("========",usr)
        books = Books.objects.get(books=usr)
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)
        



class StudentUserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('stu')
        if not token:
            raise AuthenticationFailed('unauthenticated!')

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = Student.objects.filter(id=payload['id']).first()
        serializer = LibraryUserSerializer(user)
        return Response(serializer.data)

class StudentLogoutView(APIView):  
    def post(self,request):
        response = Response()
        response.delete_cookie('stu')
        response.data={
            'msg':'Student Logout Success'
        }
        return response



