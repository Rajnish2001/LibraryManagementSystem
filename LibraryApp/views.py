from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from LibraryApp.models import Register,Books,Student,Book_issues
from LibraryApp.serializers import LibraryUserSerializer,BookSerializer,StudenSerializer,BookIssueSerializer
from LibraryApp.authentication import create_access_token,decode_access_token,create_refresh_token,decode_refresh_token
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
        
        
        # payload = {
        #     'id' : user.id,
        #     'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat': datetime.datetime.utcnow()
        # }

        # token = jwt.encode(payload, 'secret', algorithm='HS256')
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        response = Response()

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

        response.data = {
            'msg': 'Librarian Login Success' +' '+ user.name,
            # 'jwt':token
            'Access Token':access_token,
            'Refresh Token':refresh_token
        }
        # serializer = LibraryUserSerializer(user)

        # return Response(serializer.data)
        return response




class LibraryUserView(APIView):
    def get(self,request):
        # token = request.COOKIES.get('jwt')

        # if not token:
        #     raise AuthenticationFailed('unauthenticated!')

        # try:
        #     payload = jwt.decode(token,'secret',algorithms=['HS256'])

        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticated')

        # user = Register.objects.filter(id=payload['id']).first()
        # serializer = LibraryUserSerializer(user)
        # return Response(serializer.data)
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = Register.objects.filter(id=id).first()
            serializer = LibraryUserSerializer(user)

            return Response(serializer.data)

        raise AuthenticationFailed('unauthenticated')

    #For Adding Books
    def post(self,request):
        # token = request.COOKIES.get('refresh_token')
        # if not token:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')

        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')

        # user = Register.objects.filter(id=payload['id']).first()
        # if user is not None:
        #     serializer = BookSerializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return Response({'msg':'Book Added'},status=status.HTTP_201_CREATED)
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = Register.objects.filter(id=id).first()
            serializer = LibraryUserSerializer(user)
            if user is not None:
                serializer = BookSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'msg':'Book Added'},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.data)
        raise AuthenticationFailed('unauthenticated')

    # For Deleting Books
    def delete(self,request,pk=None):
        # token = request.COOKIES.get('jwt')
        # if not token:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')
        # try:
        #     payload = jwt.decode(token,'secret',algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')
        # user = Register.objects.filter(id=payload['id']).first()
        # if user is not None:
        #     query = Books.objects.get(id=pk)
        #     query.delete()
        #     return Response({'msg':query.title+' '+'Book is deleted'},status=status.HTTP_202_ACCEPTED)
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = Register.objects.filter(id=id).first()
            # serializer = LibraryUserSerializer(user)
            if user is not None:
                query = Books.objects.get(id=pk)
                query.delete()
                return Response({'msg':query.title+' '+'Book is deleted'},status=status.HTTP_202_ACCEPTED)
        raise AuthenticationFailed('unauthenticated')

    
#Books filter is pending
class BooksView(APIView):
    def get(self,request):
        # token = request.COOKIES.get('jwt')
        # if not token:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')
        # try:
        #     payload = jwt.decode(token,'secret',algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')
        # user = Register.objects.filter(id=payload['id']).first()
        # if user is None:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')

        # d = request.data['title']
        # query = Books.objects.filter(title=d)
        # serializer = BookSerializer(query,many=True)
        # return Response(serializer.data)
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = Register.objects.filter(id=id).first()
            # serializer = LibraryUserSerializer(user)
            if user is not None:
                d = request.data['title']
                query = Books.objects.filter(title=d)
                serializer = BookSerializer(query,many=True)
                return Response(serializer.data)
        raise AuthenticationFailed('unauthenticated')
    

            

# Book issue for student
    def post(self,request):
        # token = request.COOKIES.get('jwt')

        # if not token:
        #     raise AuthenticationFailed('User Unauthenticated!, Please Login first.')

        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('User Unauthenticated!, Please Login first.')

        # user = Register.objects.filter(id=payload['id']).first()

        # data = request.data

        # LibraryUser = user.id
        # data["librarian"]=LibraryUser
        # # print(data)

        # serializer = BookIssueSerializer(data=data)
        # # print(serializer)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = Register.objects.filter(id=id).first()
            # serializer = LibraryUserSerializer(user)
            if user is not None:
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
        raise AuthenticationFailed('unauthenticated')
        
#Librarian Book Search
class SearchView(APIView):
    def get(self,request):
        # token = request.COOKIES.get('jwt')
        # if not token:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')
        # try:
        #     payload = jwt.decode(token,'secret',algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')
        # user = Register.objects.filter(id=payload['id']).first()
        # if user is None:
        #     raise AuthenticationFailed('User Unauthenticated, Please Login First')

        # Search = request.GET.get('Search')
        # books = Books.objects.all()
        # if Search:
        #     books = books.filter(title__icontains=Search)
        # serializer = BookSerializer(books,many=True)
        # return Response(serializer.data)
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = Register.objects.filter(id=id).first()
            # serializer = LibraryUserSerializer(user)
            if user is not None:
                Search = request.GET.get('Search')
                print(Search)
                books = Books.objects.all()
                if Search:
                    books = books.filter(title__icontains=Search)
                serializer = BookSerializer(books,many=True)
                return Response(serializer.data)
        raise AuthenticationFailed('unauthenticated')


class LibraryUserLogoutView(APIView):  
    def post(self,request):
        response = Response()
        response.delete_cookie('refresh_token')
        response.data={
            'msg':'Success'
        }
        return response

class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'Access Token': access_token
        })


# class Searching(viewsets.ModelViewSet):
#     queryset = Books.objects.all()
#     serializer_class = BookSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['^title','=title']


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
        
       
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        response = Response()

        response.set_cookie(key='stu_refresh_token', value=refresh_token, httponly=True)

        response.data = {
            'msg': 'Student Login Success' +' '+ user.name,
            # 'jwt':token
            'Student Access Token':access_token,
            'Student Refresh Token':refresh_token
        }
        # serializer = LibraryUserSerializer(user)

        # return Response(serializer.data)
        return response


#Students can seen the list of issues books 
    def get(self,request):
        # token = request.COOKIES.get('stu')
        # if not token:
        #     raise AuthenticationFailed('unauthenticated!')

        # try:
        #     payload = jwt.decode(token,'secret',algorithms=['HS256'])

        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticated')

        # user = Student.objects.filter(id=payload['id']).first()
        # usr = Book_issues.objects.filter(student=user)
        # print(usr)
        # List = []
        # # List1=[]
        
        # data1=[]
        # for i in usr:
        #     if i is not None:
        #         expiry = i.date + datetime.timedelta(days=7)
        #         print(expiry)
        #         days = datetime.date.today()-expiry
        #         print("_______________________",days.days)
        #         fine=0
        #         if days.days > 0:
        #             print('==========',fine)
        #             fine = str(days.days*10)
        #         else:
        #             fine = '0.00'
        #         # list1=[]

        #         response = {
        #             'Books ' : i.books.title,
        #             'Book_Expiry Date' : expiry,
        #             'Fine': 'RS ' + fine 
        #         }

        #         # json_data = JSONRenderer().render(res)
        #     book = Books.objects.filter(books=i).first()

        #     data1.append(response)            
        #     List.append(book)
        #     # List.extend(list1)
        #     print(List)
        # serializer = BookSerializer(List,many=True)
        # print(serializer)
        # return Response({'data':serializer.data,"msg":data1})
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = Register.objects.filter(id=id).first()
            if user is not None:
                usr = Book_issues.objects.filter(student=user)
                print(usr)
                List = []
                # List1=[]
                
                data1=[]
                for i in usr:
                    if i is not None:
                        expiry = i.date + datetime.timedelta(days=7)
                        print(expiry)
                        days = datetime.date.today()-expiry
                        print("_______________________",days.days)
                        fine=0
                        if days.days > 0:
                            print('==========',fine)
                            fine = str(days.days*10)
                        else:
                            fine = '0.00'
                        # list1=[]

                        response = {
                            'Books ' : i.books.title,
                            'Book_Expiry Date' : expiry,
                            'Fine': 'RS ' + fine 
                        }

                        # json_data = JSONRenderer().render(res)
                    book = Books.objects.filter(books=i).first()

                    data1.append(response)            
                    List.append(book)
                    # List.extend(list1)
                    print(List)
                serializer = BookSerializer(List,many=True)
                print(serializer)
                response = Response()
                response.data = {'data':serializer.data,"msg":data1}
                # return Response({'data':serializer.data,"msg":data1})
                return response
                # def __str__(self):
                #     self.response
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        raise AuthenticationFailed('unauthenticated')
        



class StudentUserView(APIView):
    def get(self,request):
        # token = request.COOKIES.get('stu')
        # if not token:
        #     raise AuthenticationFailed('unauthenticated!')

        # try:
        #     payload = jwt.decode(token,'secret',algorithms=['HS256'])

        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticated')

        # user = Student.objects.filter(id=payload['id']).first()
        # serializer = LibraryUserSerializer(user)
        # return Response(serializer.data)
        auth = get_authorization_header(request).split()
        print(auth)        

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = Register.objects.filter(id=id).first()
            serializer = StudenSerializer(user)

            return Response(serializer.data)

        raise AuthenticationFailed('unauthenticated')

class StudentLogoutView(APIView):  
    def post(self,request):
        response = Response()
        response.delete_cookie('stu_refresh_token')
        response.data={
            'msg':'Student Logout Success'
        }
        return response

class StudentRefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('stu_refresh_token')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'Access Token': access_token
        })



