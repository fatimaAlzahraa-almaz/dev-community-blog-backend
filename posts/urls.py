from django.urls import path
from . import views
from interactions import views as interaction_views

urlpatterns=[
  path('',views.PostView.as_view(),name='posts'),
  path('<slug:slug>',views.SinglePostView.as_view(),name='single_post'),
  path('<slug:slug>/comments',views.CommentView.as_view(),name='comments'),
  path('<slug:slug>/like',interaction_views.LikeView.as_view(),name='like'),
  path('<slug:slug>/bookmark',interaction_views.BookmarkView.as_view(),name='bookmark'),
  path('<slug:slug>/comments/<int:pk>',views.SingleCommentView.as_view(),name='comment'),
  
]