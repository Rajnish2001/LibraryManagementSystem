from django.urls import path, include
from .import views

urlpatterns = [
    path('register/', views.LibraryUserRegister.as_view()),
    path('login/', views.LibraryUserLogin.as_view()),
    path('userprofile/', views.LibraryUserView.as_view()),
    path('logout/', views.LibraryUserLogoutView.as_view()),
]
