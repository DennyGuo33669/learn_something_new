# -*- coding: utf-8 -*-
# @Author  : 郭子文
# @Time    : 2021/11/12 14:25
# @联系方式 :1084558196@qq.com
# @Function:
def foo(x, *args):
    print(x)
    print(args)


# 其中2,3,4,5都给了args
foo(1, 2, 3, 4, 5)

print('****************************')


def foo_1(x, **kwargs):
    print(x)
    print(kwargs)


# 将y=1,a=2,b=3,c=4以字典的方式给了kwargs
foo_1(1, y=1, a=1, b=2, c=4)
