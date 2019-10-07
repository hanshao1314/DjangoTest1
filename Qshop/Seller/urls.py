from django.contrib import admin
from django.urls import path,re_path,include
from Seller.views import *
from django.views.decorators.cache import cache_page
urlpatterns = [
    # path('register/', cache_page(60*15)(register)),
    path('register/',register),
    path('login/', login),
    path('index/', index),
    path('logout/', logout),
    path('goods_list/', goods_list),
    re_path('goods_list/(?P<page>\d+)/(?P<status>[01])/', goods_list),
    re_path('goods_status/(?P<state>\w+)/(?P<id>\d+)/', goods_status),
    path("personal_info/", personal_info),
    path('goods_add/', goods_add),
    path('change_order/', change_order),
    path('buyer_index/', buyer_index),


    # re_path("goods_list/(?P<page>\d+)/(?P<status>[01])/", goods_list),
    re_path("goods_status/(?P<state>\w+)/(?P<id>\d+)/", goods_status),
    path("slc/",send_login_code),
    re_path("order_list/(?P<status>\d{1,2})/",order_list)



]

