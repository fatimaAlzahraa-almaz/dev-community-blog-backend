from . import views
from django.urls import path

urlpatterns=[
    path('register',views.RegisterView.as_view(),name='register'),
    path('login',views.CustomTokenObtainPairView.as_view(),name='login'),
    path('refresh',views.TokenRefreshView.as_view(),name='token_refresh'),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path('me',views.CurrentUserView.as_view(),name='current_user'),
    path('<str:username>',views.OtherUserView.as_view(),name='other_user'),
    path('<str:username>/follow',views.FollowView.as_view(),name='follow_user'),
]
