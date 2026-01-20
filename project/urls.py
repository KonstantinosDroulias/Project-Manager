from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create, name='add-project'),
    path('<int:pk>/', views.single, name='single-project'),
]