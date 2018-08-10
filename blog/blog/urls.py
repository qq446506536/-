from django.contrib import admin
from django.urls import path,re_path
from app01 import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('avatar/',views.avatar),
    # path('upload_img/',views.upload_img),
    path('form_data_upload/',views.form_data_upload),
    path('index/',views.index,name = 'index'),
    path('login/',views.login,name = 'login'),
    path('logout/',views.logout,name = 'logout'),
    re_path('^index/(?P<site_name>\w*)/$',views.homesite),
    re_path('index/(?P<site_name>\w+)/(?P<condition>category|tag|achrive)/(?P<params>.*)', views.homesite),
    path('not_found/',views.not_found),
    re_path('(?P<site_name>\w+)/articles/(?P<article_id>\d+)$', views.article_detail),
    re_path('up_down/',views.up_down),
    path('comment/',views.comment),
    path('',views.index,name='index'),
    path('back_stage/',views.back_stage,name = 'back_stage'),
    path('upload/', views.upload),
    path('delete/',views.delete),
    re_path('update/(?P<article_id>\d+)',views.update),
    path('register/',views.register,name='register'),
    path('code/', views.code_img),
    path('add_article/',views.add_article)
]
