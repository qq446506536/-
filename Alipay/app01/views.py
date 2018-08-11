import uuid
from app01 import models

from django.shortcuts import render,HttpResponse,redirect

from app01.utils.alipay import AliPay

def index(request):
    goods_list = models.Goods.objects.all()

    return render(request, 'index.html', {'goods_list': goods_list})


def buy(request,gid):
    """
    去购买 并支付
    :param request:
    :param gid:
    :return:
    """
    obj = models.Goods.objects.filter(id=gid).first()
    # 生成订单号
    no = str(uuid.uuid4())
    models.Order.objects.create(no=no,goods_id=obj.id)
    # 根据appid  支付宝网关 公钥 和私钥 生成钥跳转的地址
    # 沙箱环境地址 :https://openhome.alipay.com/platform/appDaily.htm?tab=info
    alipay =AliPay(
        appid='2016091700528841',
        app_notify_url='http://118.25.211.188:8080/check_order', # POST 发送支付状态信息
        return_url='http://118.25.211.188:8080/show',
        app_private_key_path=r'app01/RSA/private2048.txt',
        alipay_public_key_path=r'app01/RSA/public2048.txt',
        debug=True    # 默认Ture 为测试环境，False 正式环境


    )
    query_params = alipay.direct_pay(
        subject=obj.name,   # 商品的简单描述
        out_trade_no=no ,  # 商品订单号
        total_amount= obj.price   # 交易金额  (单位:元 保留2位小数)
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?%s"%(query_params) # 跳转的支付页面
    return redirect(pay_url)


def check_order(request):
    """
    post 请求   支付宝通知支付信息，让商家修改订单状态
    :param request:
    :return:
    """
    if request.method == 'POST':
        aliapy = AliPay(
            appid='2016091700528841',
            app_notify_url='http://127.0.0.1:8080/check_order',  # POST 发送支付状态信息
            return_url='http://127.0.0.1:8080/show',   # GET,将用户浏览器地址重定向回原网站
            app_private_key_path=r'app01/RSA/private2048.txt',
            alipay_public_key_path=r'app01/RSA/public2048.txt',
            debug=True  # 默认Ture 为测试环境，False 正式环境
        )
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf8')
        post_data =parse_qs(body_str)
        print(post_data,'------》post')

        post_dict = {}
        for  k,v in post_data.items():
            post_dict[k] = v[0]
        sign = post_dict.pop('sign',None)
        status = aliapy.verify(post_dict,sign)

        if status:
        #  支付成功  订单状态更新
            out_trade_no = post_dict['out_trade_no']
            models.Order.objects.filter(no=out_trade_no).update(status=2)
            return HttpResponse('success')
        else:
            return HttpResponse('支付失败')
    else:
        return HttpResponse('只支持post请求')


def show(request):
    """
    回到商户首页
    :param request:
    :return:
    """
    if request.method == "GET":
        alipay = AliPay(
            appid="2016091700528841",
            app_notify_url="http://127.0.0.1:8080/check_order/",  # POST,发送支付状态信息
            return_url="http:///127.0.0.1:8080/show/",  # GET,将用户浏览器地址重定向回原网站
            app_private_key_path=r'app01/RSA/private2048.txt',
            alipay_public_key_path=r'app01/RSA/public2048.txt',
            debug=True,  # 默认True测试环境、False正式环境
        )

        params = request.GET.dict()
        print(params,'——----》get请求')
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        if status:
            return HttpResponse('支付成功')
        else:
            return HttpResponse('失败')
    else:
        return HttpResponse('只支持GET请求')

def order_list(request):
    """
    查看所有的订单状态
    :param request:
    :return:
    """
    orders = models.Order.objects.all()
    return render(request,'order_list.html',{'orders':orders})
