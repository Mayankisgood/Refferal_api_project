from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_detail
        fields = ('name', 'email','password','referral_code', 'created_at')
                  
    def create(self, validated_data):
        print("self,validated_data",self,validated_data)
        password = make_password(validated_data.pop('password'))
        # print(password,"password")
        user_register = user_detail.objects.create(password=password,
                                                **validated_data)
        return user_register   
        