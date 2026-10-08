from django.shortcuts import get_object_or_404
from .serializers import PostSerializer, CreatePostSerializer, CommentSerializer, CreateCommentSerializer,CategorySerializer
from .models import Post, Comment,Category
from users.models import Follow
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import IsPostOwner
from .filters import PostFilter
# Create your views here.


class SinglePostView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.select_related('author','category')
    lookup_field='slug'
    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
             return CreatePostSerializer
        return PostSerializer
      
    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAuthenticated(),IsPostOwner()]
        return [AllowAny()]
      
      
class PostView(generics.ListCreateAPIView):
    filterset_class=PostFilter
    search_fields=['title']
    ordering_fields=['posted_at','title']
    ordering=['-posted_at']
    def get_serializer_class(self):
        if self.request.method in ['POST']:
             return CreatePostSerializer
        return PostSerializer
      
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        return [AllowAny()]
      
    def get_queryset(self):
        queryset=Post.objects.select_related('author','category')
        feed=self.request.query_params.get('feed','all')
         
        if feed=='following' and self.request.user.is_authenticated:
            following_ids=Follow.objects.filter(follower=self.request.user).values_list(
              'following_id',flat=True
            )
            return queryset.filter(author_id__in=following_ids)
        
        return queryset
    def perform_create(self,serializer):
        serializer.save(
            author=self.request.user
            
        )
            
class CommentView(generics.ListCreateAPIView):
    serializer_class=CommentSerializer
    orderering=['-created_at']
    def get_post(self):
        return get_object_or_404(Post,
         slug=self.kwargs['slug']  )
        
    def get_queryset(self):
        post=self.get_post()
        return Comment.objects.filter(post=post).select_related('author')
    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return CreateCommentSerializer
        return CommentSerializer
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['post']=self.get_post()
        return context
    
    def perform_create(self,serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )
        
        
class CategoryView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[AllowAny]
    

class SingleCommentView(generics.UpdateAPIView,generics.DestroyAPIView):
    serializer_class=CreateCommentSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).select_related('author','post')
    
    
    
