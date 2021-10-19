# -*- coding: utf-8 -*-
# @Author  : 郭子文
# @Time    : 2021/10/19 14:52
# @联系方式 :1084558196@qq.com
# @Function:
import datetime
import json
import random
import time
from datetime import timedelta

import requests
from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table

import sendwechat

headers = {
    'Content-Type': 'application/json',
    'Request-Source': 'PC',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


def parsing_url(url: str) -> dict:
    """
    解析所需解析门诊地址，强制要求满足格式
    https://www.114yygh.com/hospital/111/33d0296cd972d6d3cdcb9f5d92c3f680/200041482/source
    {"hosCode": url_split[4], "firstDeptCode": url_split[5], "secondDeptCode": url_split[6]}
    :param url: 门诊地址
    """

    url_split = url.split("/")
    if len(url_split) != 8:
        raise Exception("门诊解析地址无效！请核对。", url)
    else:
        md = {}
        headers["Referer"] = url

        hos_code = url_split[4]
        first_dept_code = url_split[5]
        second_dept_code = url_split[6]

        week_os_info = request_week_os_info(first_dept_code, second_dept_code, hos_code)
        md.update(week_os_info)

        os_base_properties = request_os_properties(first_dept_code, second_dept_code, hos_code)
        md.update(os_base_properties)

        return md


def request_week_os_info(first_dept_code: str, second_dept_code: str, hos_code: str) -> dict:
    """
    获取当前一星期的预约状况
    """

    body = {
        "firstDeptCode": first_dept_code,
        "secondDeptCode": second_dept_code,
        "hosCode": hos_code,
        "week": 1
    }

    request_url = "https://www.114yygh.com/web/product/list"
    response = requests.post(request_url, headers=headers, data=json.dumps(body)).json()

    if response["resCode"] != 0:
        raise Exception("获取门诊预约信息异常，请前往检查！", request_url, body, response)

    return response["data"]


def request_os_properties(first_dept_code: str, second_dept_code: str, hos_code: str) -> dict:
    """
    通过请求地址获取门诊信息
    """

    format_url = "https://www.114yygh.com/web/department/hos/detail?firstDeptCode={}&secondDeptCode={}&hosCode={}"

    request_url = format_url.format(first_dept_code, second_dept_code, hos_code)
    response = requests.get(request_url, headers=headers).json()

    if response["resCode"] != 0:
        raise Exception("获取门诊基础信息异常，请检查！", request_url, response)

    return response["data"]


def parsing_url_with_list(urls: list) -> list:
    """
    将多个门诊地址进行解析并返回
    :param urls: 门诊集合列表
    :return:
    """

    os_parsed_list = []
    for url in urls:
        os_parsed_list.append(parsing_url(url))

    return os_parsed_list


def all_info_of_table(request_os_list: list) -> Table:
    parsed_data = parsing_url_with_list(request_os_list)
    print(parsed_data)
    aJson = json.dumps(parsed_data)
    cc = ''.join(aJson)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    if cc.find("AVAILABLE") >= 0:
        print("YES")
        sendwechat.send()
    else:
        print("NO")

    # 最近一周的日期 %Y-%m-%d
    week_of_name = []
    now = datetime.datetime.now()
    for value in range(1, 8):
        next_day = now + timedelta(days=value)
        week_of_name.append(next_day.strftime("%Y-%m-%d"))

    table = Table(box=box.ROUNDED, title="[aquamarine3]114 网上预约实时监控({})".format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

    table.add_column('[light_sea_green]医院', justify="center")
    table.add_column('[light_sea_green]科部', justify="center")
    table.add_column('[light_sea_green]门诊', justify="center")

    for value in week_of_name:
        table.add_column('[light_sea_green]' + value, justify="center")

    available = []

    for data in parsed_data:

        week_of_dict = {0: "[red]未知", 1: "[red]未知", 2: "[red]未知", 3: "[red]未知", 4: "[red]未知", 5: "[red]未知",
                        6: "[red]未知"}

        hospital_dict = {"hosName": data["hosName"],
                         "firstDeptName": data["firstDeptName"],
                         "secondDeptName": data["secondDeptName"]}

        yuyue_available = []
        for index, value in enumerate(week_of_name):
            for calendars in data["calendars"]:
                if value == calendars["dutyDate"]:
                    if calendars["status"] == "NO_INVENTORY":
                        # 无号
                        week_of_dict[index] = "[red3]无号"
                    elif calendars["status"] == "AVAILABLE":
                        # 可约
                        week_of_dict[index] = "[green]可预约"

                        vc = [value, "可预约"]
                        yuyue_available.append("* " + ' | '.join(vc) + "\n")
                    elif calendars["status"] == "SOLD_OUT":
                        # 约满
                        week_of_dict[index] = "[indian_red]已约满"
                    elif calendars["status"] == "TOMORROW_OPEN":
                        # 即将放号
                        week_of_dict[index] = "[steel_blue1]即将放号"
                    else:
                        week_of_dict[index] = "[red]未知状态"
                    break

        hospital_dict["yuyue"] = yuyue_available
        available.append(hospital_dict)
        table.add_row(data["hosName"], data["firstDeptName"], data["secondDeptName"],
                      week_of_dict[0], week_of_dict[1],
                      week_of_dict[2], week_of_dict[3],
                      week_of_dict[4], week_of_dict[5],
                      week_of_dict[6])

    return table


if __name__ == '__main__':
    console = Console(color_system='256', style=None)

    url = "https://www.114yygh.com/hospital/122/d3bbb5cb1ac8a26829dd4e23b88f839a/200044272/source"
    cookie = "imed_session=n0LhBgDqKZ2Lx3ScHH5xUFX8dFo9GEhC_5448744; imed_session=n0LhBgDqKZ2Lx3ScHH5xUFX8dFo9GEhC_5448744; imed_session_tm=1634623408583; agent_login_img_code=73e94e75a41d457eb3797f5722acfe76; cmi-user-ticket=Fa2jZJ-C6Gk_P3YkSms3bdKGasT2w4VQPsvlFA..; imed_session=n0LhBgDqKZ2Lx3ScHH5xUFX8dFo9GEhC_5448744; secure-key=b47f7e31-b92e-4352-a386-c8d2d9f780cc"
    headers["Cookie"] = cookie
    os_list = []
    os_list.append(url)

    os_data = None
    with console.status("[light_goldenrod3]正在首次加载数据...[/]", spinner="moon"):
        os_data = all_info_of_table(os_list)

    # 首次加载由外部完成，normal为正常加载sleep 5s
    normal = False
    with Live(console=console, screen=True, auto_refresh=False) as live:
        while True:
            if normal:
                time.sleep(20 + random.randint(1, 10))
                os_data = all_info_of_table(os_list)

            live.update(os_data, refresh=True)
            normal = True