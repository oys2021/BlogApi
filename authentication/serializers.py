from rest_framework import serializers
from authentication.models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    image_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model=CustomUser
        fields=['id','full_name','username','password','bio','profile_image','image_absolute_url','role']

    def get_image_absolute_url(self,obj):
        request=self.context.get('request')

        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    def create(self,validated_data):
        profile_image = validated_data.pop('profile_image', None)
        full_name=validated_data.pop('full_name', None)
        username=validated_data.pop('username', None)
        bio=validated_data.pop('bio', None)
        role=validated_data.pop('role', None)
        password = validated_data.pop('password') 

        user = CustomUser(
        full_name=full_name,
        username=username
        )
        user.set_password(password)

        if profile_image:
            user.profile_image =profile_image

        if bio:
            user.bio = bio

        if role:
            user.role = role


        user.save()
        return user 
    
    def update(self, instance, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        full_name = validated_data.pop('full_name', None)
        role = validated_data.pop('role', None)
        bio=validated_data.pop('bio', None)
        username=validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_image is not None:
            instance.image = profile_image
        
        if full_name is not None:
            instance.full_name = full_name
            
        if role is not None:
            instance.role = role

        if bio is not None:
            instance.bio = bio

        if username is not None:
            instance.username = username
        
        instance.save()
        return instance
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','full_name','username','bio','profile_image','role']
        read_only_fields = ['id']








