from django.urls import path
from .import views


urlpatterns =[
    path('', views.index, name= 'index'),
    path('post/', views.post, name= 'post'),
    path('homepage/', views.HomeView.as_view(), name= 'homepage'),
    path('room/<int:pk>/', views.portfolio, name= 'portfolio'),
    path('send/<int:pk>/', views.send_message, name= 'send_message'),
    path('myroom/<str:portfolio_name>/', views.my_room, name= 'my_room')
]