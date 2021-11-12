# -*- coding: utf-8 -*-
# @Author  : 郭子文
# @Time    : 2021/11/12 16:50
# @联系方式 :1084558196@qq.com
# @Function:

def print_func(name):
    def p_name():
        print("I am " + name)

    # 调用内嵌函数
    return p_name()


if __name__ == '__main__':
    print_func('Denny')
