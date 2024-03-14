from django.urls import path
from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path('',views.Routes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.register,name='register'),
    path('CurrentUser/',views.currentuser,name='current_user'),
    path('Posts_User/',views.current_post_user,name="PostOfUser"),
    path('Profile/',views.user_profile,name="Profile"),
    
]
