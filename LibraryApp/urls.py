from django.urls import path, include
from .import views

urlpatterns = [
    path('register/', views.LibraryUserRegister.as_view()),
    path('login/', views.LibraryUserLogin.as_view()),
    path('userprofile/', views.LibraryUserView.as_view()),
    path('userprofile/<int:pk>/', views.LibraryUserView.as_view()),
    path('logout/', views.LibraryUserLogoutView.as_view()),
    path('studentregister/', views.StudentView.as_view()),
    path('studentlogin/', views.StudentLoginView.as_view()),
    path('studentprofile/', views.StudentUserView.as_view()),
    path('studentlogout/', views.StudentLogoutView.as_view()),
    path('viewbooks/', views.BooksView.as_view()),
]
