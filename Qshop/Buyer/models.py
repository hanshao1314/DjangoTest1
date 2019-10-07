from django.db import models
from Seller.models import LoginUser

class Payorder(models.Model):
    """
      订单表
      订单状态
      0 未支付
      1 已支付
      2 待发货
      3 待收货
      4/5 完成/拒收
      """
    order_number=models.CharField(max_length=32)
    order_data=models.DateTimeField(auto_now=True)
    # order_status=models.IntegerField()
    order_total=models.FloatField(blank=True,null=True)
    order_user=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)

class OrderInfo(models.Model):
    """
    订单详情页
    订单详页
    0：未支付
    1：已支付
    2：待收货
    3/4 完成、拒绝
    """
    order_id=models.ForeignKey(to=Payorder,on_delete=models.CASCADE)
    goods_id=models.IntegerField()
    goods_picture=models.CharField(max_length=32)
    goods_name=models.CharField(max_length=32)
    goods_count=models.IntegerField()
    goods_price=models.FloatField()
    goods_total_price=models.FloatField()
    order_status = models.IntegerField(default=0)
    store_id=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)

from django.db.models import Manager
class CartManage(Manager):
    def adds(self,id):
        cart=Cart.objects.get(id=id)
        cart.goods_number+=1
        cart.goods_total+=cart.goods_price
        cart.save()

class Cart(models.Model):
    """
      商品名称
      商品数量（购买数量）
      商品价格
      商品图片
      商品总价（单个商品）
      商品id
      用户
      """
    good_name=models.CharField(max_length=32)
    goods_number=models.IntegerField()
    goods_price=models.FloatField()
    goods_picture=models.CharField(max_length=32)
    goods_total=models.FloatField()
    goods_id=models.IntegerField()
    cart_user=models.IntegerField()

    objects=CartManage()

"""
一个订单，三件商品，假如一件商品确认发货，其他两件未发货
订单状态？
前端展示问题
后端修改问题
"""