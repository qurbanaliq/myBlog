from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("create/", views.post_create, name="post_create"),
    path("<int:pk>/detail", views.post_detail, name="post_detail")
]