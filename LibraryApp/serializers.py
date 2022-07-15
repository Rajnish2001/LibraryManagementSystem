from LibraryApp.models import Register,Books,Student
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'name', 'dob', 'gender', 'email', 'degree', 'password']

        extra_kwargs = {
            'password':{'write_only':True}
        }


    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id','title','auther','price']

class StudenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'dob', 'gender', 'email', 'degree', 'password']

        extra_kwargs = {
            'password':{'write_only':True}
        }


    # def create(self, validated_data):
    #     password = validated_data.pop('password',None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance