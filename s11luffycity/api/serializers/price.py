# !user/bin/python3
# Author:Mr.Yuan
# -*- coding:utf-8 -*-
# @time: 2018/8/8 17:52

from rest_framework import serializers
from app01 import models

class PriceSerializer(serializers.ModelSerializer):
    valid_period = serializers.CharField(source='get_valid_period_display')
    id = serializers.CharField()
    class Meta:
        model = models.PricePolicy
        fields = ['id','valid_period','price',]