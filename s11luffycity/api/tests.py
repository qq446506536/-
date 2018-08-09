from django.test import TestCase

from redis import Redis

cnon = Redis(port=6379, host='192.168.11.139')

cnon.set('YuanYong', '袁勇')

# Create your tests here.

print(len(cnon.keys('YuanYong')))

print(cnon.get('YuanYong').decode('utf8'))
