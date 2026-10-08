from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post
# Create your models here.

User=get_user_model()

class Bookmark(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookmarks')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='bookmarks')
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints=[
        models.UniqueConstraint(
          fields=['user','post'],
          name='unique_bookmark',
        )
      ]
    
    def __str__(self):
        return f'{self.user.username} bookmarked {self.post.title}'
      

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[
          models.UniqueConstraint(
            fields=['user','post'],
            name='unique_like',
          )
        ]
    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'




