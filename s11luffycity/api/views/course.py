# !user/bin/python3
# Author:Mr.Yuan
# -*- coding:utf-8 -*-
# @time: 2018/8/7 15:37

from django.shortcuts import render,HttpResponse

from rest_framework.viewsets import ViewSet
from api import serializers as api_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.pagination import PageNumberPagination
from api.utlils.response import BaseResponse
from app01 import models
from api.serializers.course import  CourseModeSerializer,CourseSerializer,DgreeCourseSeria,Deg,D5,D6,D7,D8

class CourseView(APIView):

    def get(self,request,*args,**kwargs):
        ret = BaseResponse()

        try:
            queryset = models.Course.objects.filter(degree_course__isnull=True).all()
            # 分页
            # page = PageNumberPagination()
            # course_list = page.paginate_queryset(queryset,request,self)
            # 分页之后的结果执行序列化
            ser = CourseSerializer(instance=queryset,many=True)
            ret.data = ser.data

            print(ret.data)
        except Exception as e :
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)


class CourseDetailView(APIView):
    def get(self,request,pk,*args,**kwargs):
        response = {'code':100,'data':None,'error':None}
        try:
            course = models.Course.objects.get(id=pk)
            ser = CourseSerializer(instance=course)
            response['data'] = ser.data
        except Exception as e :
            response['code'] = 500
            response['error'] = '获取数据失败'
        return Response(response)


class DgressCorseView(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            dgree_course = models.DegreeCourse.objects.all()
            print(dgree_course)
            ser = DgreeCourseSeria(instance=dgree_course,many=True)
            ret.data = ser.data
        except Exception as e :
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)

# d. 查看id=1的学位课对应的所有模块名称
class D4View(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.Course.objects.filter(degree_course_id=1).all()
            ser = Deg(instance=course_obj, many=True)
            ret.data = ser.data
        except Exception as e:
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)


# e.获取id = 2的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
class D5View(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.Course.objects.filter(id=2,degree_course__isnull=True).first()
            print(course_obj,'66666666666666')
            ser = D5(instance=course_obj)
            ret.data = ser.data
        except Exception as e:
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)


class D6View(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            course_obj =models.Course.objects.filter(id=2,degree_course__isnull=True).first()
            print(course_obj,'66666666666666')
            ser = D6(instance=course_obj)
            ret.data = ser.data
        except Exception as e:
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)


class D7View(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.OftenAskedQuestion.objects.all()
            print(course_obj, '66666666666666')
            ser = D6(instance=course_obj, many=True)
            ret.data = ser.data
        except Exception as e:
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)



class D8View(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.CourseOutline.objects.filter(course_detail__course__degree_course__isnull=True,course_detail__course_id=2).first()
            print(course_obj, '66666666666666')
            ser = D7(instance=course_obj)
            ret.data = ser.data
        except Exception as e:
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)




class D9View(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.CourseChapter.objects.filter(course__degree_course__isnull=True,course_id=2).first()
            print(course_obj, '66666666666666')
            ser = D8(instance=course_obj)
            ret.data = ser.data
        except Exception as e:
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return Response(ret.dict)


