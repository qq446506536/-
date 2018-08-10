#!user/bin/python3
#Author:Mr.Yuan
#-*- coding:utf-8 -*-
#@time: 2018/7/21 19:49

from django.utils.deprecation import MiddlewareMixin

class Authmad1(MiddlewareMixin):
    white_list = ['/login/','/register/','/index/','/(?P<site_name>\w+)/articles/(?P<article_id>\d+)$/','/code/','/favicon.ico/','/logout/','/aelx的站点/articles/2']
    def process_request(self,request):
        from django.shortcuts import redirect,HttpResponse
        next_url = request.path_info
        print(next_url,666666666666)
        if next_url  in self.white_list:
            return
        elif next_url not in self.white_list and not request.user.username:
            return redirect('/login/')
        # else:
        #     print(1111111111111)
        #     return redirect("/login/?next={}".format(next_url))

