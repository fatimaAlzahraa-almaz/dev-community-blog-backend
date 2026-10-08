from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from .models import Like ,Bookmark
from rest_framework.response import Response
from posts.serializers import PostSerializer

# Create your views here.


class LikeView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get_post(self):
        return get_object_or_404(Post,slug=self.kwargs['slug'])
    def post(self,request,*args,**kwargs):
        post=self.get_post()
        _,created=Like.objects.get_or_create(user=request.user,post=post)
        if not created :
            return Response({"detail":"You have already liked this post."},status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "Post liked successfully."},
            status=status.HTTP_201_CREATED,
        )
        
    def delete(self,request,*args,**kwargs):
        post=self.get_post()
        deleted,_=Like.objects.filter(user=request.user,post=post).delete()
        if not deleted :
            return Response({"detail": "You have not liked this post."},status=status.HTTP_400_BAD_REQUEST)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

class BookmarkView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get_post(self):
        return get_object_or_404(Post,slug=self.kwargs['slug'])
    def post(self,request,*args,**kwargs):
        post=self.get_post()
        _,created=Bookmark.objects.get_or_create(user=request.user,post=post)
        if not created :
            return Response({"detail":"You have already bookmarked this post."},status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "Post bookmarked successfully."},
            status=status.HTTP_201_CREATED,
        )
        
    def delete(self,request,*args,**kwargs):
        post=self.get_post()
        bookmarked,_=Bookmark.objects.filter(user=request.user,post=post).delete()
        if not bookmarked :
            return Response({"detail": "You have not bookmarked this post."},status=status.HTTP_400_BAD_REQUEST)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
       
       
class BookmarkListView(generics.ListAPIView):
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated]
    ordering=['-bookmarks__created_at']
    
    def get_queryset(self):
        return Post.objects.filter(bookmarks__user=self.request.user).select_related('author','category').order_by('-bookmarks__created_at')

