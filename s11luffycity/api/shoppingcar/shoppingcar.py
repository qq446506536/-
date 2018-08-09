# !user/bin/python3
# Author:Mr.Yuan
# -*- coding:utf-8 -*-
# @time: 2018/8/8 17:02
import json

from django.shortcuts import HttpResponse
from django.conf import settings

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser

from api.utlils.response import BaseResponse
from app01 import models
from api.serializers import course, price
from redis import Redis

COON = Redis(port=6379, host='192.168.11.139')
USERID = 1


class ShoppingCarView(ViewSetMixin, APIView):
    # parser_classes = [JSONParser,]   这个是 解析器   限制前端传过来的请求头的格式 ，这样写就只能是json格式的数据类型   非json数据类型的时候 拿不到数据
    SHOP_CAR = {}
    SHOPPING_CAR = {
        '用户1': {
            1: {
                'title': 'xxxx',
                'price': 1,
                'price_list': [
                    {'id': 11, },
                    {'id': 22},
                    {'id': 33},
                ]
            },
            3: {},
            5: {}
        },
        2: {},
        3: {},
    }

    def create(self, request, *args, **kwargs):
        try:
            ret = BaseResponse()
            """
            购物车  假设都是专题课 因为这个是可控的
            传过来的<QueryDict: {'courseid': ['1'], 'priceid': ['1']}>
            :param request:
            :param args:
            :param kwargs:
            :return:
            """
            """
                 1. 接受用户选中的课程ID和价格策略ID
                 2. 判断合法性
                     - 课程是否存在？
                     - 价格策略是否合法？
                 3. 把商品和价格策略信息放入购物车 SHOPPING_CAR
        
                 注意：用户ID=1
                 """
            # 1.接受用户选中的课程ID和价格策略ID
            """
                相关问题：
                    a. 如果让你编写一个API程序，你需要先做什么？
                        - 业务需求
                        - 统一数据传输格式
                        - 表结构设计
                        - 程序开发
                    b. django restful framework的解析器的parser_classes的作用？
                        根据请求中Content-Type请求头的值，选择指定解析对请求体中的数据进行解析。
                        如：
                            请求头中含有Content-type: application/json 则内部使用的是JSONParser，JSONParser可以自动去请求体request.body中
                            获取请求数据，然后进行 字节转字符串、json.loads反序列化；
        
                    c. 支持多个解析器（一般只是使用JSONParser即可）
        
            """
            print(request.POST, "--->request.post")
            # print(request.body)
            print(request.data)
            price_id = request.data.get('priceid')
            course_id = request.data.get('courseid')
            course_obj = models.Course.objects.filter(id=course_id).first()
            # price_obj = models.PricePolicy.objects.filter(id=price_id).first()
            # if course_obj and price_obj:
            #     price_res = course_obj.price_policy.all().filter(id=price_id).first()  # 目标课程对应的目标价格
            #
            #     if price_res:
            #         price_all = course_obj.price_policy.all()  # 目标课程对应的所有价格
            #
            #         price_obj_rea = price.PriceSerializer(instance=price_obj)   # 目标课程序列化
            #         price_all_rea = price.PriceSerializer(instance=price_all, many=True) # 目标课程对应的所有价格 序列化
            #         course_obj_rea = course.CourseModeSerializer(instance=course_obj)    # 目标课程的对应的一个价格 序列化
            #         # print(price_obj_rea.data,price_all_rea.data,course_obj_rea.data)
            #         print('目标课程的价格信息————>', price_obj_rea.data)
            #         print('目标课程的所有价格信息————>', price_all_rea.data)
            #         print('目标课程信息————>', course_obj_rea.data)
            #         ret.data = [price_all_rea.data, price_all_rea.data, course_obj_rea.data]
            #         price_list = []
            #         for i in price_all_rea.data:
            #             print(dict(i))
            #             price_list.append(dict(i))
            #         msg = {'title': course_obj_rea.data.get('name'),
            #                'price': price_obj_rea.data.get('price'),
            #                'price_list': price_list
            #                }
            #
            #         self.SHOPPING_CAR['用户1'][1] = msg
            #         print(self.SHOPPING_CAR)
            #         return Response(self.SHOPPING_CAR)
            #     else:
            #         ret.code = 1111
            #         ret.data = '价格和课程不匹配'
            #
            #
            # else:
            #     ret.code = 111111
            #     ret.data = '价格或者课程不存在'
            if not course_obj:
                ret.code = 1111
                ret.data = '课程不存在'
                return Response(ret.dict)
            price_all = course_obj.price_policy.all()  # 目标课程对应的所有价格策略
            print(price_all)
            price_dict = {}  # 创建一个存放目标课程对应的所有价格策略 的字典
            for item in price_all:
                temp = {
                    'id': item.id,
                    'price': item.price,
                    'valid_period': item.valid_period,
                    'valid_period_display': item.get_valid_period_display()

                }
                price_dict[item.id] = temp
            print(price_dict)
            # print(type(price_id))
            if int(price_id) not in price_dict:
                ret.data = '价格与不匹配，fuck off'
                ret.code = 44444
                return Response(ret.dict)
            # key = 'shoppingcar_%s_%s' % (USERID, course_id)
            key = settings.SHOPCAR_FORMAT.format(USERID,course_id)
            print(key,'----->')
            if key and len(COON.keys(key)) >= 100:
                ret.code = 9999
                ret.data = '购物车的数量已满，请付款后再继续购买'
                return Response(ret.dict)
            COON.keys(key)
            COON.hset(key, 'id', course_obj.id)
            COON.hset(key, 'name', course_obj.name)
            COON.hset(key, 'img', course_obj.course_img)
            COON.hset(key, 'default', price_id)
            COON.hset(key, 'price_dict', json.dumps(price_dict))
            # print(COON.info(),"---->")
            COON.expire(key, 20 * 60)  # 创建完之后 20 分钟之类删除，也就是提醒用户20分钟之内付款  否则购物车清空
            print(COON.keys())
            ret.code = 66
            ret.data = '购买成功'
        except Exception as  e:
            ret.data = '加入购物车失败'
            ret.code = 1000
        return Response(ret.dict)

    def list(self, *args, **kwargs):
        """
        查看购物车信息
        :param args:
        :param kwargs:
        :return:
        """
        try:
            ret = BaseResponse()
            shopping_car_course_list = []
            # key = 'shoppingcar_%s_%s' % (USERID, '*')
            key = settings.SHOPCAR_FORMAT.format(USERID, "*")
            user_key_list = COON.keys(pattern=key)  # 取到这个用户对应的所有课程字典 对应的键
            for key in user_key_list:
                # 对应的每个键值 去取每个课程对应的信息 和价格列表
                temp = {
                    'id': COON.hget(key, 'id').decode('utf8'),
                    'name': COON.hget(key, 'name').decode('utf8'),
                    'img': COON.hget(key, 'img').decode('utf8'),
                    'default': COON.hget(key, 'default').decode('utf8'),
                    'price_dict': json.loads(COON.hget(key, 'price_dict').decode('utf8')),
                }
                shopping_car_course_list.append(temp)
            ret.data = shopping_car_course_list
        except Exception as e:
            ret.data = '查看失败'
            ret.code = 00000
        return Response(ret.dict)

    def update(self, request, *args, **kwargs):
        """
        修改用户的选中的价格策略
        拿到价格策略id 然后更改 课程信息对应的默认价格id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            ret = BaseResponse()
            priceid = request.data.get('priceid')
            courseid = request.data.get('courseid')
            # print(type(priceid),courseid)
            priceid = str(priceid) if priceid else None   # 如果不转成str 在后面会找不到
            # key = 'shoppingcar_%s_%s' % (USERID, courseid)
            key = settings.SHOPCAR_FORMAT.format(USERID, courseid)
            if not COON.exists(key):
                ret.data = '课程不存在'
                ret.code = 44444
                return Response(ret.dict)
            price_dict = json.loads(COON.hget(key, 'price_dict').decode('utf8'))
            if priceid not in price_dict:
                ret.data = '价格策略不存在'
                ret.code = 4444
                return Response(ret.dict)
            COON.hset(key, 'default', priceid)
            COON.expire(key, 20 * 60)  # 在20分钟之后删除
            ret.code = 666
            ret.data = '修改成功'
        except Exception as  e:
            ret.code = 0000
            ret.data = '失败'
        return Response(ret.dict)

    def destroy(self, request, pk, *args, **kwargs):
        """
        删除课程
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            ret = BaseResponse()
            # key = 'shoppingcar_%s_%s' % (USERID, pk)
            key = settings.SHOPCAR_FORMAT.format(USERID, pk)
            COON.delete(key)
            ret.data = '删除成功'
            ret.code = 66
        except Exception as e:
            ret.data = '失败'
            ret.code = 000
        return Response(ret.dict)
