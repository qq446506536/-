# !user/bin/python3
# Author:Mr.Yuan
# -*- coding:utf-8 -*-
# @time: 2018/8/8 17:02
from django.shortcuts import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from rest_framework.views import APIView
from api.utlils.response import BaseResponse
from rest_framework.response import Response
from app01 import models
from api.serializers import course,price
class ShoppingCarView(ViewSetMixin, APIView):
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
        ret = BaseResponse()
        """
        购物车  假设都是专题课 因为这个是可控的
        传过来的<QueryDict: {'courseid': ['1'], 'priceid': ['1']}>
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        print(request.data)
        price_id = request.data.get('priceid')
        course_id = request.data.get('courseid')
        course_obj = models.Course.objects.filter(id=course_id).first()
        price_obj = models.PricePolicy.objects.filter(id=price_id).first()
        if course_obj and price_obj :
            price_res = course_obj.price_policy.all().filter(id=price_id).first()  # 目标课程对应的目标价格

            if price_res :
                price_all = course_obj.price_policy.all()                          # 目标课程对应的所有价格

                price_obj_rea = price.PriceSerializer(instance=price_obj)
                price_all_rea = price.PriceSerializer(instance=price_all,many=True)
                course_obj_rea = course.CourseModeSerializer(instance=course_obj)
                # print(price_obj_rea.data,price_all_rea.data,course_obj_rea.data)
                print('目标课程的价格信息————>',price_obj_rea.data)
                print('目标课程的所有价格信息————>',price_all_rea.data)
                print('目标课程信息————>', course_obj_rea.data)
                ret.data = [price_all_rea.data,price_all_rea.data,course_obj_rea.data]
                price_list = []
                for i in price_all_rea.data:
                    print(dict(i))
                    price_list.append(dict(i))
                msg = {'title':course_obj_rea.data.get('name'),
                       'price': price_obj_rea.data.get('price'),
                       'price_list':price_list
                       }


                self.SHOPPING_CAR['用户1'][1]=msg
                print(self.SHOPPING_CAR)
                return Response(self.SHOPPING_CAR)
            else:
                ret.code  = 1111
                ret.data = '价格和课程不匹配'


        else:
            ret.code = 111111
            ret.data = '价格或者课程不存在'


        return Response(ret.dict)

    def list(self, *args, **kwargs):
        return HttpResponse('hehe')
