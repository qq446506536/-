#!user/bin/python3
#Author:Mr.Yuan
#-*- coding:utf-8 -*-
#@time: 2018/7/12 8:48

from django import template
from ..models import Category,Tag,Article,UserInfo,Blog
from django.db.models import Count,Avg,Max

register=template.Library()


@register.inclusion_tag("left_regin.html")
def querry_date(blog):
    tag_list = Tag.objects.filter(blog=blog).annotate(count=Count('article__nid')).values("title",'count')

    print(tag_list)
    category_list = Category.objects.filter(blog=blog).annotate(
        count=Count('article__category_id')).values('title', 'count')
    print(category_list)
    date_list = Article.objects.filter(user_id=blog.userinfo.nid).extra(
        select={'y_m_date': "DATE_FORMAT(create_time,'%%Y/%%m')"}).values("y_m_date").annotate(
        count=Count('pk')).values('y_m_date', 'count')
    print(11111111111,date_list)
    return {'blog':blog,'tag_list':tag_list,'category_list':category_list,'date_list':date_list}




 # {'blog':blog,'tag_list':tag_list,'category_list':category_list,'date_list':date_list}

