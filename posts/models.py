from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your models here.

User=get_user_model()

class Category(models.Model):
    title=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.title


class Post(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(unique=True,blank=True)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='posts')
    img=models.ImageField(upload_to='post_images/',blank=True,null=True , max_length=255,)
    posted_at=models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            max_length=self._meta.get_field('slug').max_length
            base_slug=slugify(self.title)
            if not base_slug:
                base_slug='post'
            base_slug=base_slug[:max_length]
            slug=base_slug
            counter=1
            while Post.objects.filter(slug=slug).exists():
                suffix=f'-{counter}'
                slug=f'{base_slug[:max_length-len(suffix)]}{suffix}'
                counter+=1
                 
            self.slug=slug
        super().save( *args, **kwargs)
    
    def __str__(self):
        return f'{self.title} by {self.author.username}'
      
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    parent=models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
