from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserDetailView.as_view(), name='user-detail'),
    path('upload/', views.UploadImageView.as_view(), name='upload'),
]