# !user/bin/python3
# Author:Mr.Yuan
# -*- coding:utf-8 -*-
# @time: 2018/8/6 20:37
from django.conf.urls import url
from api import views
from api.views import course
from api.shoppingcar import shoppingcar

urlpatterns = [
    url(r'^courses/$', course.CourseView.as_view()),
    url(r'^courses/(?P<pk>\d+)/$', course.CourseDetailView.as_view()),
    url(r'^degreecourse/$', course.DgressCorseView.as_view()),
    url(r'^course_name/$', course.D4View.as_view()),
    url(r'^d5/$', course.D5View.as_view()),
    url(r'^d6/$', course.D6View.as_view()),
    url(r'^d7/$', course.D8View.as_view()),
    url(r'^d8/$', course.D9View.as_view()),
    url(r'^shopcar/$', shoppingcar.ShoppingCarView.as_view({'get': 'list', 'post': 'create','put': 'update',})),
    url(r'^shopcar/(?P<pk>\d+)$', shoppingcar.ShoppingCarView.as_view({'delete': 'destroy'})),

]

# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'course', views.Course)
# router.register(r'detail',views.CourseDetail,base_name=[])
#
#
# urlpatterns += router.urls
