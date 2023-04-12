from django.urls import path, re_path
from .import views


urlpatterns =[
    path('', views.index, name= 'index'),
    path('test/', views.test, name= 'test'),
    path('post/', views.post, name= 'post'),
    path('popup_box_view/<str:product>/<str:session_id>/', views.popup_box_view, name='popup_box_view'),
    path('homepage/', views.HomeView.as_view(), name= 'homepage'),
    path('product_list/', views.product_list, name= 'product_list'),
    path('room/<int:pk>/', views.portfolio, name= 'portfolio'),
    path('send/<int:pk>/', views.send_message_api, name= 'send_message'),
    path('support-page/<str:session_id>/', views.support_page_view, name= 'support_page'),
    path('support_chat_view/<str:session_id>/', views.support_chat_view, name= 'support_page'),
    path('admin_support_page_view/<str:session_id>/', views.admin_support_page_view, name= 'admin_support_page_viewss'),
    path('chatresponse/<str:session_id>/', views.chatresponse_view, name= 'chatresponse'),

    # path('chat/', views.chat_box_view, name='chat-box-view'),
    #login  chat 100014
    re_path(r'^chat/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.chat_box_view, name='chat-box'),
    re_path(r'^chatbox/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.chat_box_userinfo_view, name='chat-box'),

    ##
    re_path(r'^chat/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.popup_box_view, name='chat-box'),

    #   re_path(r'^support-chat-box/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9]{32})/)?$', views.support_chat_box_view, name='support-chat-box'),

]

#
#   https://ll04-finance-dowell.github.io/100018-dowellWorkflowAi-testing/#/?session_id=wvpouhbr4ov07bf3yfhyoziucz4roi8d&id=100093