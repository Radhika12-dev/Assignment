from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', TaskListCreateAPIView.as_view(), name= 'task_list_create'),
    path('tasks/<int:pk>', TaskDetailAPIView.as_view(), name='task_detail')
]