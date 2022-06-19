from dataclasses import fields
from datetime import date
from rest_framework import serializers
from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
from django_countries.serializer_fields import CountryField
import random
from django.contrib.auth.models import Group



def genrate_password(first_name , last_name):
          random_num = random.random()
          password = f'{first_name}-{random_num}-{last_name}'
          return password


class UserSerializer(serializers.ModelSerializer):
     phone_number = PhoneNumberField()
     country_code = CountryField()

     class Meta:
          model = CustomUser
          exclude = ('username','password')

     def create(self, validated_data):
          user = self.context.get('user')
          user_obj = CustomUser(**validated_data,user_id=user.id)
          user_obj.username = user_obj.first_name + " " +  user_obj.last_name
          user_obj.password = genrate_password(user_obj.first_name,user_obj.last_name)
          my_group = Group.objects.get(name='Admin') 
          user_obj.groups.add(my_group)
          if user_obj.birthdate > date.today():
               raise serializers.ValidationError({"errors": {"birthdate":[{"error":"birth date not in the past"}]}})     
          else:     
               try:
                    user_obj.save()
                    return user_obj
               except Exception as e :  
                    raise serializers.ValidationError({"errors": {"error":[{"error":e}]}})     











class StausSerializer(serializers.ModelSerializer):
     class Meta:
          model = CustomUser
          fields = '__all__'
