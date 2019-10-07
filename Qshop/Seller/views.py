import hashlib  # 导入哈希函数包
from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
import datetime,time
from Seller.models import *  #从models模块中导入所有定义类和函数方法

# 定义一个装饰器，
def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie_email=request.COOKIES.get("email")
        session_email=request.session.get("email")
        if cookie_email and session_email and cookie_email==session_email:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Seller/login/")
    return inner

# 定义哈希函数，对于密码进行加密
def setPassword(password):
    md5=hashlib.md5()  #对于密码进行加密
    md5.update(password.encode())   #：密码进行编码
    result=md5.hexdigest()
    return result   #返回加密后的结果

# 定义用户注册函数，
def register(request):
    error_message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # 先判断用户邮箱是否已经注册
        if email:
            # :首先检测email有没有
            user = LoginUser.objects.filter(email=email).first()
            if not user:
                new_user = LoginUser()
                new_user.email = email
                new_user.email = email
                new_user.password = setPassword(password)
                new_user.save()
            else:
                error_message = "邮箱已经被注册，请登录"
        else:
            error_message = "邮箱不可以为空"
    return render(request, "seller/register.html", locals())


from django.views.decorators.cache import cache_page
@cache_page(60*15)   #使用缓存，缓存的寿命15分钟
# 登录账号
def login(request):
    error_message=""
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        code=request.POST.get("valid_code")  #检验验证码
        # 首先检测email有没有
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                db_password=user.password
                password=setPassword(password)
                if db_password==password:
                    # 检测验证码
                    # 获取验证码
                    codes=Valid_Code.objects.filter(code_user=email).order_by("-code_time").first()
                    # 校验验证码是否存在，是否过期，是否被使用
                    now=time.mktime(datetime.datetime.now().timetuple())
                    db_time=time.mktime(codes.code_time.timetuple())
                    t=(now-db_time)/60
                    if codes and codes.code_state==0 and t<=5 and codes.code_content.upper()==code.upper():
                        response=HttpResponseRedirect("/Seller/index/")
                        response.set_cookie("email",user.email)
                        response.set_cookie("user_id",user.id)
                        request.session["email"]=user.email
                        return response
                    else:
                        error_message="验证码错误"
                else:
                    error_message="密码错误"
            else:
                error_message="用户不存在"
        else:
            error_message="邮箱不可以为空"
    return render(request,"seller/login.html",locals())

def logout(request):
    response=HttpResponseRedirect("/login/")
    keys=request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session["email"]
    return response

@loginValid
def index(request):
    # goods_type=GoodsType.objects.all()  #：获取所有类型
    # result=[]
    # for ty in goods_type:
    #     # :按照生产日期对对应类型的商品进行排序
    #     goods=ty.goods_set.order_by("-goods_pro_time")
    #     if len(goods)>=4:  #：进行条件判断
    #         goods=goods[:4]
    #         result.append({"type":ty,"goods_list":goods})
    return render(request,"seller/index.html",locals())

@loginValid
def goods_list(request,status,page=1):
    user_id=request.COOKIES.get("user_id")
    user=LoginUser.objects.get(id=int(user_id))
    page=int(page)
    if status=="1":
        goodses=Goods.objects.filter(goods_store=user,goods_status=1)
    elif status=="0":
        goodses=Goods.objects.filter(goods_store=user,goods_status=0)
    else:
        goodses=Goods.objects.all()
    all_goods=Paginator(goodses,10)
    goods_list=all_goods.page(page)
    return render(request, "seller/goods_list.html", locals())

@loginValid
def goods_status(request,state,id):
    id=int(id)
    goods=Goods.objects.get(id=id)
    if state=="up":
        goods.goods_status=1
    elif state=="down":
        goods.goods_status =0
    goods.save()
    url=request.META.get("HTTP_REFERER","/goods_list/1/1")
    return HttpResponseRedirect(url)

@loginValid
def personal_info(request):
    user_id=request.COOKIES.get("user_id")
    user=LoginUser.objects.get(id=int(user_id))
    if request.method=="POST":
        user.email=request.POST.get("email")
        user.gender=request.POST.get("gender")
        user.age=request.POST.get("age")
        user.phone_number=request.POST.get("phone_number")
        user.address=request.POST.get("address")
        user.photo=request.POST.get("photo")
        user.save()
    return render(request,"seller/personal_info.html",locals())

@loginValid
def goods_add(request):
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        goods = Goods()
        # 常规保存
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_count = data.get("goods_count")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_date = data.get("goods_safe_date")
        goods.goods_pro_time = data.get("goods_pro_time")  # 出厂日期格式必须是yyyy-mm-dd格式
        goods.goods_status = 1
        # 保存外键类型
        goods_type_id = int(data.get("goods_type"))
        goods.goods_type = GoodsType.objects.get(id=goods_type_id)
        # 保存图片
        picture = files.get("picture")
        goods.picture = picture
        # 保存对应的卖家
        user_id = request.COOKIES.get("user_id")
        goods.goods_store = LoginUser.objects.get(id=int(user_id))
        goods.save()
    return render(request, "seller/goods_add.html", locals())

def base(request):
    return render(request,"seller/base.html",locals())


"""————2019.9.17——————"""
import random,json
#生成随机数
def random_code(len=6):
    """
    生成6位数的随机验证码
    :param len:
    :return:
    """
    string="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    valid_code="".join([random.choice(string) for i in range(len)])
    return valid_code
# 发送验证码
import json
import requests
from Qshop.settings import DING_URL
def sendDing(content,to=None):
    headers={
        "Content-Type":"application/json",
        "Charset":"utf-8"
    }
    requests_data={
        "msgtype":"text",
        "text":{
            "content":content
        },
        "at":{
            "atMobiles":[
            ],
            "isAtAll":True
        }
    }
    if to:
        requests_data["at"]["atMobiles"].append(to)
        requests_data["at"]["isAtAll"]=False
    else:
        requests_data["at"]["atMobiles"].clear()
        requests_data["at"]["isAtAll"] = True
    sendData=json.dumps(requests_data)
    response=requests.post(url=DING_URL,headers=headers,data=sendData)
    content=response.json()
    return content
from Seller.models import *
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def send_login_code(request):
    result={
        "code":200,
        "data":""
    }
    if request.method=="POST":
        email=request.POST.get("email")
        code=random_code()
        c=Valid_Code()
        c.code_user=email
        c.code_content=code
        c.save()
        send_data="%s的验证码是%s:'明月照我心，我心与明月；'"%(email,code)
        sendDing(send_data)
        result["data"]="发送成功"
    else:
        result["code"]=400
        result["data"]="请求错误"
    return JsonResponse(result)


def order_list(request,status):
    """

    :param request:
    :param status:
    :return:
    """
    status=int(status)
    user_id=request.COOKIES.get("user_id")  #:获取店铺id
    store=LoginUser.objects.get(id=user_id)  #获取店铺信息
    store_order=store.orderinfo_set.filter(order_status=status).order_by("-id")   #：获取店铺对用的订单
    return render(request,"seller/order_list.html",locals())


from Buyer.models import OrderInfo
def change_order(request):
    order_id=request.GET.get("order_id")
    order_status=request.GET.get("order_status")
    order=OrderInfo.objects.get(id=order_id)
    order.order_status=int(order_status)
    order.save()
    url = request.META.get("HTTP_REFERER", "/order_list/1/")
    return HttpResponseRedirect(url)
    # return JsonResponse({"data":"修改成功"})


def buyer_index(request):
    return render(request,"buyer/index.html")