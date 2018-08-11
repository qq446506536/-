from django.db import models

# Create your models here.
# 商品表
class Goods(models.Model):
    name = models.CharField(max_length=32)
    price = models.FloatField()


#  订单表
class  Order(models.Model) :
    no = models.CharField(max_length=64)   # 订单号
    goods = models.ForeignKey(to='Goods')
    status_choice = ((1,'未支付'),(2,'已支付'))
    status = models.IntegerField(choices=status_choice,default=1)
