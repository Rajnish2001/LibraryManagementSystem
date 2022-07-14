from LibraryApp.models import Register
from rest_framework import serializers

class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'usertype', 'name', 'dob', 'gender', 'email', 'degree', 'password']

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


