# -*- coding: utf-8 -*-
# @Author  : 郭子文
# @Time    : 2021/9/14 16:17
# @联系方式 :1084558196@qq.com
# @Function:
from pathlib import Path

now_path = Path.cwd()
home_path = Path.home()

print("当前工作目录",now_path,type(now_path))
print("home目录",home_path,type(home_path))
