from django.urls import path, re_path
from .import views


urlpatterns =[
    path('', views.index, name= 'index'),
    path('test/', views.test, name= 'test'),
    path('post/', views.post, name= 'post'),
    path('homepage/', views.HomeView.as_view(), name= 'homepage'),
    path('room/<int:pk>/', views.portfolio, name= 'portfolio'),
    path('send/<int:pk>/', views.send_message_api, name= 'send_message'),
    path('support-page/<str:session_id>/', views.support_page_view, name= 'support_page'),
    path('chatresponse/<str:session_id>/', views.chatresponse_view, name= 'chatresponse'),

    #path('chat/<str:session_id>/<str:product>/', views.chat_box_view, name='chat-box-view'),

    re_path(r'^chat/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.chat_box_view, name='chat-box'),
    #   re_path(r'^support-chat-box/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9]{32})/)?$', views.support_chat_box_view, name='support-chat-box'),
    
    #Update message API ednpoint
    path('api/edit_message/<int:pk>/', edit_message,name='edit_message')

]

#
#   https://ll04-finance-dowell.github.io/100018-dowellWorkflowAi-testing/#/?session_id=wvpouhbr4ov07bf3yfhyoziucz4roi8d&id=100093