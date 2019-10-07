from Buyer.views import *
from django.urls import path,re_path
from django.contrib import admin

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/',index),
    path('logout/',logout),
    path('goods_list/',goods_list),
    re_path('detail/(?P<id>\d+)/',goods_detail),
    # path('base/',base),
    path('user_info/',user_center_info),
    path('uco/', user_center_order),
    path('pay_order/',pay_order),
    path('pay_order_more/',pay_order_more),
    path('alipay/',AlipayViews),
    path('pay_result/',pay_result),
    path('seller_index/',seller_index),


    path('user_center_site/', user_center_site),
    path('add_cart/',add_cart),
    path('cart/',cart),
    path('gt/',get_task),
    path('mtv/',middle_test_view),

]