from rest_framework import serializers
from .models import Post, Comment, Category
from django.contrib.auth import get_user_model

User=get_user_model()



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','profile_img']
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        read_only_fields=['id','title']
        

class CommentSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    class Meta:
        model=Comment
        fields=['id', 'content', 'author','created_at','parent']
        read_only_fields=['id','created_at','parent','content','author']
        
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','content','parent','created_at']
        read_only_fields=['id','parent','created_at']
        
    def validate(self,attrs):
        parent=attrs.get('parent')
        #we send context from the view
        post=self.context.get('post')
        
        if parent and parent.post_id!=post.id:
            raise serializers.ValidationError({
               "parent": "This comment does not belong to this post."
            })
            
        return attrs
    
    
        
class CreatePostSerializer(serializers.ModelSerializer):
    remove_img=serializers.BooleanField(write_only=True,required=False,default=False)
    class Meta:
        model=Post
        fields=['id','title','slug','content','author','posted_at','category','img','remove_img']
        read_only_fields=['id','posted_at','slug','author']
    def create(self, validated_data):
        validated_data.pop('remove_img', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        remove_img=validated_data.pop('remove_img', False)
        if remove_img:
            instance.img.delete(save=False)
            instance.img=None
        return super().update(instance, validated_data)
      
      

      
class PostSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    category=CategorySerializer(read_only=True)
    likes_count=serializers.SerializerMethodField()
    comments_count=serializers.SerializerMethodField()
    bookmarks_count=serializers.SerializerMethodField()
    is_liked=serializers.SerializerMethodField()
    is_bookmarked=serializers.SerializerMethodField()
    class Meta:
       model=Post
       fields=['id','title','slug','content','posted_at','img','author','category','likes_count','comments_count','bookmarks_count','is_liked','is_bookmarked']
    
    def get_likes_count(self,obj):
        return obj.likes.count()
    
    def get_comments_count(self,obj):
         return obj.comments.count()
     
    def get_bookmarks_count(self,obj):
         return obj.bookmarks.count()
    
    def get_is_liked(self,obj):
        user=self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
    
    def get_is_bookmarked(self,obj):
        user=self.context.get('request').user
        if user.is_authenticated:
            return obj.bookmarks.filter(user=user).exists()
        return False