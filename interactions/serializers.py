from rest_framework import serializers
from .models import Bookmark, Like
from posts.models import Post


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
      model=Like
      fields=['id','user','post','created_at']
      read_only_fields=['id','created_at','user','post']
      
      
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
      model=Bookmark
      fields=['id','user','post','created_at']
      read_only_fields=['id','created_at','user','post']