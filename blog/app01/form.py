#!user/bin/python3
#Author:Mr.Yuan
#-*- coding:utf-8 -*-
#@time: 2018/7/15 12:10
import re
from .models import UserInfo
from django import forms
from django.forms import Widget,widgets
from django.core.exceptions import ValidationError,NON_FIELD_ERRORS
wid = widgets.TextInput(attrs={'class':'form_control'})
class Userform(forms.Form):
    username = forms.CharField(label='用户名',widget=widgets.TextInput(attrs={"class":"form-control",}),error_messages={'required':'不能为空哦','invalid':'输入的太短'})
    pwd = forms.CharField(min_length=4,max_length=16,label='密码',widget=widgets.PasswordInput(attrs={'class':'form-control'}),)
    ensure_pwd = forms.CharField(min_length=4,max_length=16,label='确认密码',widget=widgets.PasswordInput(attrs={'class':'form-control'}),error_messages={'required':'不能为空哦','invalid':'格式不正确'})
    email = forms.EmailField(widget=widgets.TextInput(attrs={'class':'form-control'}),label='邮箱',error_messages={'required':'不能为空哦','invalid':'格式不正确'})
    telephone = forms.IntegerField(widget=widgets.TextInput(attrs={'class':'form-control'}),label='电话',error_messages={'required':'不能为空哦','invalid':'请输入正确的电话号码'})
    def clean_username(self):
        val = self.cleaned_data.get('username')
        user_val_dic =self.cleaned_data  #拿到的是字典
        # print(888888888,user_val_dic)
        user = UserInfo.objects.values('username')
        # print(9999999999999,user)#这个是querryset

        if user_val_dic in user :
            raise ValidationError('用户名已经存在，请重新输入')
        else:

            if not val.isdigit and len(val) > 4 and len(val) < 16:
                return val
            elif val.isdigit():
                raise ValidationError('用户名不能是纯数字')
            elif len(val)< 4:
                raise ValidationError('您输入的太短，请重新输入')
            elif len(val) > 16:
                raise ValidationError('您输入的超过最大限制16位')

    def clean_telephone(self):
        val = self.cleaned_data.get('telephone')
        # print('*************',val,type(val))
        res = re.findall('0?(13|14|15|17|18|19)[0-9]{9}',str(val))
        if  res:
            return val
        else:raise ValidationError('请输入正确的电话号码')



    def clean(self):
        '''
        全局钩子 验证
        :return:
        '''
        pwd = self.cleaned_data.get('pwd')
        ensure_pwd = self.cleaned_data.get('ensure_pwd')
        print('###########',pwd,ensure_pwd)
        if pwd and ensure_pwd and pwd != ensure_pwd:
            # print(66666666666)
            raise ValidationError('两次输入的不一样')
        # elif len(pwd)==0 or len(ensure_pwd)==0:
        #     raise ValidationError('不能为空哦')
        else:
            # print(7777777)
            return self.cleaned_data
