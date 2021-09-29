# -*- coding: utf-8 -*-
# @Author  : 郭子文
# @Time    : 2021/9/29 10:32
# @联系方式 :1084558196@qq.com
# @Function:
from faker import Faker

faker = Faker('zh_CN')
print(f"name:{faker.name()}")
print(f"address:{faker.address()}")
print(f"text:{faker.text()}")