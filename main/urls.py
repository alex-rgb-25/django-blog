from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from main.forms import MyAuthForm

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("<int:blog_id>/", views.blog, name="blog"),
    path("create/", views.create, name="create"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=MyAuthForm), name='login'), 
    path("<int:blog_id>/edit/", views.edit, name="edit"),
    path("<int:blog_id>/delete/", views.delete, name="delete"),
    path("<int:blog_id>/like/", views.like, name="like"),
    path("<int:blog_id>/like2", views.like2, name="like2"),
    ]