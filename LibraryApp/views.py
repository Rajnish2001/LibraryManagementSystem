from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from LibraryApp.models import Register,Books,Student,Book_issues
from LibraryApp.serializers import LibraryUserSerializer,BookSerializer,StudenSerializer,BookIssueSerializer
import jwt, datetime
from rest_framework.filters import SearchFilter
from rest_framework import viewsets

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
        if user is None:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')

        

        d = request.data['title']
        query = Books.objects.filter(title=d)
        serializer = BookSerializer(query,many=True)
        return Response(serializer.data)
    

            

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
        
#Librarian Book Search
class SearchView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')
        user = Register.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('User Unauthenticated, Please Login First')

        Search = request.GET.get('Search')
        books = Books.objects.all()
        if Search:
            books = books.filter(title__icontains=Search)
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)







class LibraryUserLogoutView(APIView):  
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'msg':'Success'
        }
        return response

class Searching(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^title','=title']


#
# class Filter_Searching_view(ListAPIView):
#     def list(self,request):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('User Unauthenticated!, Please Login first.')
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('User Unauthenticated!, Please Login first.')
#         user = Register.objects.filter(id=payload['id']).first()
#         if user is None:
#             raise AuthenticationFailed('User Unauthenticated!, Please Login first.')

#         d = request.data['title']
#         print(d)
#         query = Books.objects.filter(title=d)
#         print(query)
#         serializer = BookSerializer(query,many=True)
#         return Response(serializer.data)







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

#Students can seen the list of issues books 
    def get(self,request):
        token = request.COOKIES.get('stu')
        if not token:
            raise AuthenticationFailed('unauthenticated!')

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = Student.objects.filter(id=payload['id']).first()
        usr = Book_issues.objects.filter(student=user)
        print(usr)
        List = []
        # List1=[]
        
        data1=[]
        for i in usr:
            if i is not None:
                expiry = i.date + datetime.timedelta(days=-1)
                print(expiry)
                days = datetime.date.today()-expiry
                fine = (days.days*10)
                # list1=[]

                response = {
                    'Books ' : i.books.title,
                    'Book_Expiry Date' : expiry,
                    'Fine': 'RS ' + str(fine) 
                }

                # json_data = JSONRenderer().render(res)
            book = Books.objects.filter(books=i).first()

            data1.append(response)            
            List.append(book)
            # List.extend(list1)
            print(List)
        serializer = BookSerializer(List,many=True)
        print(serializer)
        return Response({'data':serializer.data,"msg":data1})
        



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



