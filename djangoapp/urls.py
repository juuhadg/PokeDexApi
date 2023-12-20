from django.urls import path
from . import views

urlpatterns = [
    path('', views.getUsers),
    path('create', views.addUser),
    path('get/<str:id>', views.getUser),
    path('update/<str:id>', views.updateUser),
    path('delete/<str:id>', views.deleteUser),
]
