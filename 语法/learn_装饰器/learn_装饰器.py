# -*- coding: utf-8 -*-
# @Author  : 郭子文
# @Time    : 2021/11/12 16:18
# @联系方式 :1084558196@qq.com
# @Function:

from time import time


def timer(func):
    def f(x, y=10):
        before = time()
        rv = func(x, y)
        after = time()
        print('time taken: ', after - before)
        return rv

    return f


@timer
def add(x, y=10):
    return x + y


@timer
def sub(x, y=10):
    return x - y


print('add(10)', add(10))
print('add(20, 30)', add(20, 30))
print('add("a", "b")', add("a", "b"))
print('sub(10)', sub(10))
print('sub(20, 30)', sub(20, 30))
