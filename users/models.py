from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=100)
    bio=models.TextField(blank=True)
    profile_img=models.ImageField(upload_to='profile_images/',blank=True,null=True)
    
    def __str__(self):
        return self.username
      
      

class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow',
            ),
            models.CheckConstraint(
                condition=~models.Q(follower=models.F('following')),
                name='prevent_self_follow',
            ),
        ]
    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
