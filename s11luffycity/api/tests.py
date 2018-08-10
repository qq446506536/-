from django.test import TestCase

from redis import Redis

# cnon = Redis(port=6379, host='192.168.11.139')
COON = Redis(port=6379, host='192.168.11.139')

COON.set('YuanYong', '袁勇')
COON.mget()
# Create your tests here.

print(len(COON.keys('YuanYong')))

print(COON.get('YuanYong').decode('utf8'))
