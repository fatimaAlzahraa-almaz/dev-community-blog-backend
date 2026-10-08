from rest_framework import serializers
from .models import User,Follow
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm=serializers.CharField(write_only=True)
    class Meta:
      model=User
      fields=['username','name','email','password','password_confirm']
      extra_kwargs = {
            "password": {"write_only": True},
        }
      
    def validate(self,data):
        if data['password']!=data['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm':'Passwords do not match'}
              )
        return data
        
    def create(self,validated_data):
        validated_data.pop('password_confirm')
        user=User.objects.create_user(**validated_data)
        return user
        
class UserSerializer(serializers.ModelSerializer):
    followers_count=serializers.SerializerMethodField()
    following_count=serializers.SerializerMethodField()
    is_following=serializers.SerializerMethodField()
    class Meta:
      model=User
      fields=['id','username','name','bio','profile_img','date_joined','is_following','followers_count','following_count']
      
      read_only_fields=[
        'id',
        'username',
        'date_joined',
        'is_following',
        'followers_count',
        'following_count'
      ]
       
    def get_followers_count(self,obj):
        return obj.followers.count()
      
       
    def get_following_count(self,obj):
        return obj.following.count()
        
    def get_is_following(self,obj):
        request=self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Follow.objects.filter(
            follower=request.user,
            following=obj
        ).exists()
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username from required fields since we're using email
        self.fields.pop('username', None)
    
    def validate(self, attrs):
        email = attrs.pop('email')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(email=email)
            attrs['username'] = user.username
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'No active account found with the given credentials'
            )
        
        return super().validate(attrs)
    
