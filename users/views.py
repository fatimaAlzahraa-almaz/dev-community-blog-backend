from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer,UserSerializer,CustomTokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import User,Follow
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from core import settings
# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer
    
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token=serializer.validated_data['refresh']
        access_token=serializer.validated_data['access']
        response=Response(
            {
                'access':access_token,
            },
             status=status.HTTP_200_OK,
        )
        refresh_lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=int(refresh_lifetime.total_seconds()),
            httponly=True,
            secure=True,
            samesite='None',
            path='/api/users/'
        )
        return response
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token=request.COOKIES.get('refresh_token')
        if token :
            try:
                refresh_token=RefreshToken(token)
                refresh_token.blacklist()
            except TokenError:
                pass
        
        response=Response(
            {
                'detail':'logged out successfully'
            },
            status=status.HTTP_200_OK   
        )
        response.delete_cookie(key='refresh_token',path='/api/users/',
          samesite='Lax')
        
        return response                     
            
        
        

class TokenRefreshView(TokenRefreshView):
    serializer_class=TokenRefreshSerializer
    
    def post(self,request,*args,**kwargs):
        refresh_token=request.COOKIES.get('refresh_token')
         
        if not refresh_token:
            return Response(
                {'detail':'Refresh token not found'},
                 status=status.HTTP_401_UNAUTHORIZED,
            )
        
        serializer=self.get_serializer(
            data={
                'refresh':refresh_token
            }
        )
        serializer.is_valid(raise_exception=True)
        
        response=Response(
            {
                'access':serializer.validated_data['access'],
            },
             status=status.HTTP_200_OK,
        )
        
        if 'refresh' in serializer.validated_data:
            refresh_lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        
            response.set_cookie(
            key='refresh_token',
            value=serializer.validated_data['refresh'],
            max_age=int(refresh_lifetime.total_seconds()),
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/api/users/'
        )
            
        return response




class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    def get_object(self):
        return self.request.user
    
class OtherUserView(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field = "username"
    
    
class FollowView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    
    def get_target_user(self):
        return get_object_or_404(User,username=self.kwargs['username'])
    def post(self, request, *args, **kwargs):
        target_user=self.get_target_user()
        if request.user==target_user:
            return Response({"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST)
        _,created= Follow.objects.get_or_create(follower=request.user,following=target_user)
        
        if not created:
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"detail": "Successfully followed."},
            status=status.HTTP_201_CREATED
        )
        
    
    def delete(self, request, *args, **kwargs):
        target_user=self.get_target_user()
        if request.user==target_user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        deleted,_=Follow.objects.filter(follower=request.user,following=target_user).delete()
        
        if not deleted:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
           
            status=status.HTTP_204_NO_CONTENT
        )
    

