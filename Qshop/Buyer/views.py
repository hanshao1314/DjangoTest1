from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from Seller.models import *
from Seller.views import setPassword
from Buyer.models import *
import time, datetime
from alipay import AliPay


def loginValid(fun):
    def inner(request, *args, **kwargs):
        cookie_user = request.COOKIES.get("username")
        session_user = request.session.get("username")
        if cookie_user and session_user and cookie_user == session_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner


def register(request):
    # error_message=""
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")

        user = LoginUser()
        user.username = username
        user.password = setPassword(password)
        user.email = email
        user.save()
        return HttpResponseRedirect("/Buyer/login/")
    return render(request, "buyer/register.html")


# def login(request):
#     error_message = ""
#     if request.method == "POST":
#         password = request.POST.get("pwd")
#         email = request.POST.get("email")
#         user = LoginUser.objects.filter(email=email).first()
#         if user:
#             db_password = user.password
#             password = setPassword(password)
#             if db_password == password:
#                 response = HttpResponseRedirect("/Buyer/index/")
#                 response.set_cookie("username", user.username)
#                 response.set_cookie("user_id", user.id)
#                 request.session["username"] = user.username
#                 return response
#     return render(request, "buyer/login.html")

def logout(request):
    url = request.META.get("HTTP_REFERER", "/Buyer/index/")
    response = HttpResponseRedirect(url)
    for k in request.COOKIES:
        response.delete_cookie(k)
    del request.session["username"]
    return response

def index(request):
    goods_type = GoodsType.objects.all()  # ：获取所有类型
    result = []
    for ty in goods_type:
        # :按照生产日期对对应类型的商品进行排序
        goods = ty.goods_set.order_by("-goods_pro_time")
        if len(goods) >= 4:  # ：进行条件判断
            goods = goods[:4]
            result.append({"type": ty, "goods_list": goods})
    return render(request, "buyer/index.html", locals())


def goods_list(request):
    """
    type：代表请求的类型
        t:按照类型查询
            keywords:必须是类型id
        k:按照关键字查询
    :keyword:代表请求的关键字
    :param request:
    :return:
    """
    request_type = request.GET.get("type")  # ：获取请求的类型 t类型查询 k 关键字查询
    keyword = request.GET.get("keywords")  # 查询的内容 t类型 k为类型id k类型k为关键字
    goods_list = []  # 返回的结果
    if request_type == "t":  # t类型查询
        if keyword:
            id = int(keyword)
            goods_type = GoodsType.objects.get(id=id)  # ：先查询类型
            goods_list = goods_type.goods_set.order_by("-goods_pro_time")  # 再查询类对应的商品
    elif request_type == "k":
        if keyword:
            goods_list = Goods.objects.filter(goods_name__contains=keyword).order_by(
                "-goods_pro_time")  # ：模糊查询商品名称含有关键字的商品
    if goods_list:  # ：限定推荐的条数
        lenth = len(goods_list) / 5
        if lenth != int(lenth):
            lenth += 1
        lenth = int(lenth)
        recommend = goods_list[:lenth]
    return render(request, "buyer/goods_list.html", locals())


def goods_detail(request, id):
    goods = Goods.objects.get(id=int(id))
    return render(request, "buyer/detail.html", locals())


@loginValid
def user_center_info(request):
    return render(request, "buyer/user_center_info.html", locals())


def pay_order(request):
    goods_id = request.GET.get("goods_id")
    count = request.GET.get("count")
    if goods_id and count:
        # 保存订单表，但是保存总价
        order = Payorder()
        order.order_number = str(time.time()).replace(".", "")
        order.order_data = datetime.datetime.now()
        # order.order_status = 0    #  2019.9.19这段代码需要删除
        order.order_user = LoginUser.objects.get(id=int(request.COOKIES.get("user_id")))  # 订单对应的马买家
        order.save()
        # 保存订单详情
        # 查询商品的信息
        goods = Goods.objects.get(id=int(goods_id))
        order_info = OrderInfo()
        order_info.order_id = order
        order_info.goods_id = goods.id
        order_info.goods_picture = goods.picture
        order_info.goods_name = goods.goods_name
        order_info.goods_count = int(count)
        order_info.goods_price = goods.goods_price
        order_info.goods_total_price = goods.goods_price * int(count)
        order_info.store_id = goods.goods_store  #:商品卖家，goods.goods_store本身就是一条卖家数据
        order_info.save()
        order.order_total = order_info.goods_total_price
        order.save()
    return render(request, "buyer/pay_order.html", locals())


from Qshop.settings import alipay_public_key_string, alipay_private_key_string


def AlipayViews(request):
    order_number = request.GET.get("order_number")
    order_total = request.GET.get("total")
    # 实例化支付
    alipay = AliPay(
        appid="2016101200667755",
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )
    # 实例化订单
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_number,  # 订单号
        total_amount=str(order_total),  # 支付金额，是字符串
        subject="生鲜交易",  # 支付主题
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",  #:返回结果的地址
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/",  # ：订单状态发生改变后，返回的地址
    )  # 网页支付订单
    # 拼接收款地址 = 支付宝网关+订单返回参数
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)


def pay_result(request):
    out_trade_no = request.GET.get("out_trade_no")
    if out_trade_no:
        order = Payorder.objects.get(order_number=out_trade_no)  #总的的订单号
        order.orderinfo_set.all().update(order_status=1) #当前订单所有的详情订单
        # order.order_status = 1
        order.save()
    return render(request, "buyer/pay_result.html", locals())


# """——————————2019--9--16————————————————————"""
@loginValid
def add_cart(request):
    result = {
        "code": 200,
        "data": ""
    }
    if request.method == "POST":
        id = int(request.POST.get("goods_id"))
        count = int(request.POST.get("count", 1))

        goods = Goods.objects.get(id=id)
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_number = count
        cart.goods_price = goods.goods_price
        cart.goods_picture = goods.picture
        cart.goods_total = goods.goods_price * count
        cart.goods_id = id
        cart.cart_user = request.COOKIES.get("user_id")
        cart.save()
        result["data"] = "加入购物车成功"
    else:
        result["code"] = 500
        result["data"] = "请求方式错误"
    return JsonResponse(result)


def cart(request):
    """
      返回当前用户购物车当中的商品以-id
      """
    user_id = request.COOKIES.get("user_id")
    goods = Cart.objects.filter(cart_user=int(user_id)).order_by("-id")
    count = goods.count()
    return render(request, "buyer/cart.html", locals())

@loginValid
def user_center_order(request):
    user_id=request.COOKIES.get("user_id")
    user=LoginUser.objects.get(id=int(user_id))
    order_list=user.payorder_set.order_by("-order_data")
    return render(request,"buyer/user_center_order.html",locals())


@loginValid
def pay_order_more(request):
    data = request.GET
    data_item = data.items()
    request_data = []
    for key,value in data_item:
        if key.startswith("check_"):
            goods_id = key.split("_", 1)[1]  #:圆括号的1,是以下划线切一次
            count = data.get("count_" + goods_id)
            request_data.append((int(goods_id), int(count)))
    if request_data:
        # 保存订单表，但是保存总价
        order = Payorder()
        order.order_number = str(time.time()).replace(".", "")
        order.order_data = datetime.datetime.now()
        # order.order_status = 0   #9.19号删除
        order.order_user = LoginUser.objects.get(id=int(request.COOKIES.get("user_id")))  # 订单对应的买家
        order.save()
        # 保存订单详情
        # 查询商品的信息
        order_total = 0
        for goods_id,count in request_data:
            goods = Goods.objects.get(id=int(goods_id))
            order_info = OrderInfo()
            order_info.order_id = order
            order_info.goods_id = goods.id
            order_info.goods_picture = goods.picture
            order_info.goods_name = goods.goods_name
            order_info.goods_count = int(count)
            order_info.goods_price = goods.goods_price
            order_info.goods_total_price = goods.goods_price * int(count)
            order_info.store_id = goods.goods_store # 商品卖家，goods.goods_store本身就是一条卖家数据
            order_info.save()
            order_total += order_info.goods_total_price  # 总价计算
        order.order_total = order_total
        order.save()
    return render(request, "buyer/pay_order.html", locals())

# """——————2019.9.18——————"""

from CeleryTask.tasks import add

def get_task(request):
    num1=request.GET.get("num1",1)
    num2=request.GET.get("num2",2)
    add.delay(int(num1),int(num2))
    return JsonResponse({"data":"success"})

from django.http import HttpResponse
# def middle_test_view(request):
#     def hello():
#         return HttpResponse("hello world")
#     print("I am view")
#     return JsonResponse({"data":"hello world"})

# from django.http import HttpResponse
# def middle_test_view(request):
#     def hello():
#         return HttpResponse("hello world")
#     rep=HttpResponse("你好")
#     rep.render=hello
#     return rep

def middle_test_view(request):
    print("I am view")
    return JsonResponse({"data":"hello world"})

def seller_index(request):
    return render(request,"seller/index.html")

def user_center_site(request):
    return render(request,"buyer/user_center_site.html")


from django.core.cache import cache
def cacheTest(request):
    user=cache.get("user") #从缓存里面获取数据
    if not user:  #如果获取为None
        user=LoginUser.objects.get(id=1)
        cache.set("user",user,30)  #将用户数据存入缓存，缓存时间30秒

    return JsonResponse({"data":"hello world"})

"""————————2019.9.20——————————"""

import logging
collcet=logging.getLogger('django')
def login(request):
    error_message = ""
    if request.method == "POST":
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        user = LoginUser.objects.filter(email=email).first()
        if user:
            db_password = user.password
            password = setPassword(password)
            if db_password == password:
                response = HttpResponseRedirect("/Buyer/index/")
                response.set_cookie("username", user.username)
                response.set_cookie("user_id", user.id)

                collcet.debug("%s is login"%user.username)
                return response
    return render(request, "buyer/login.html")




