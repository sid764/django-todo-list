from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("see", views.see, name="see"),
    path("add", views.add, name="add"),
    path("delete", views.delete, name="delete")
]
