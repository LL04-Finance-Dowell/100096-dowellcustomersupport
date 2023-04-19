from django.urls import path, re_path
from .import views


app_name = 'customer_support'


urlpatterns = [
    #   path('post/', views.post, name= 'post'),
    #   path('homepage/', views.HomeView.as_view(), name= 'homepage'),
    #   path('support_chat_view/<str:session_id>/', views.support_chat_view, name= 'support_page'),
    #   re_path(r'^support-page/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.support_page_view, name= 'support_page_old'),

    path('', views.index, name= 'index'),
    re_path('test/', views.test, name= 'test'),     #(?:session_id=(?P<session_id>[a-z0-9])/)?$

    path('room/<int:room_id>/', views.room_details, name= 'room-details'),
       # this is for message list, or send message
    path('product_list/', views.product_list, name= 'product_list'),

    re_path(r'^room_list/(?P<product>[0-9\w-]+)', views.room_list, name= 'room_list'),# room_list for provided product

    re_path(r'^dowell-api/create-room/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.createRoomAPI, name= 'create-room-API'),    #    create reoom API

    re_path(r'^extension-chat/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])&prdct=(?P<prdct>[0-9\w-]+)/)?$', views.extension_chat_box_view, name='extension_chat_box_view'),# Not live

    path('send/<int:pk>/', views.send_message_api, name= 'send_message'),
    re_path(r'^chat/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.chat_box_view, name='chat-box'),


    path('send_message/<int:pk>/', views.send_msg_api_2, name= 'send_message_2'),
    re_path(r'^chat-box/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.chatbox_withDU_view, name='popup-chat-box'),


    path('customer-support/', views.admin_support_page_view, name='support-page'),  # entry

    path('main-support/', views.main_support_page, name='main-support-page'),

    path('living-lab-support/', views.living_lab_support_view, name='living-lab-support'),      ## entry

    path('main-living-lab-support/', views.main_living_lab_support_page, name='main-living-lab-support-page'),

    #   re_path(r'^customer-support-second/(?:session_id=(?P<session_id>[a-z0-9])/)?$', views.admin_support_page_sec_view, name='support-page-2'),
    #   re_path(r'^support-chat-box/(?P<product>[0-9\w-]+)/(?:session_id=(?P<session_id>[a-z0-9]{32})/)?$', views.support_chat_box_view, name='support-chat-box'),
    #   path('chat/<str:session_id>/<str:product>/', views.chat_box_view, name='chat-box-view'),product_room_list
]

#
#   https://ll04-finance-dowell.github.io/100018-dowellWorkflowAi-testing/#/?session_id=wvpouhbr4ov07bf3yfhyoziucz4roi8d&id=100093