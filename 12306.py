
"""

爬虫基本流程
一.数据来源分析
1.明确需求:明确采集网站以及数据
网址；https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E4%B8%8A%E6%B5%B7,SHH&ts=%E5%B9%BF%E5%B7%9E,GZQ&date=2024-09-06&flag=N,N,Y
数据：车次信息
2.抓包分析：通过浏览器开发者工具分析数据位置
 -打开开发者工具：F12或鼠标右键点击检查
 -点击查询按钮
 -查票接口：https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2024-09-06&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT
二.代码实现
1.发送请求；模拟浏览器对于url发送请求
2.获取数据：获取浏览器返回的相应数据
3.解析数据：提取我们需要的内容
4.保存数据：本次只用展示即可

"""
# 导入模块
import requests
# 导入格式化输出模块
from pprint import pprint
# 导入漂亮的制表
from prettytable import PrettyTable
# 导入json模块
import json
'''
查票功能
1.输入出发地
2.输入目的地
3.输入出发时间
根据输入的城市 -> 通过city.json 找到对应的城市字母
'''
# 读取json文件
f = open('city.json',encoding='utf-8').read()
# 转成json字典
city_data = json.loads(f)

from_city = input('请输入出发地：')
to_city = input('请输入目的地：')
date = input('请输入出发时间(如：2024-01-01)：')
print(city_data[from_city])
print(city_data[to_city])

# 请求网址
url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={city_data[from_city]}&leftTicketDTO.to_station={city_data[to_city]}&purpose_codes=ADULT'

# 模拟浏览器
headers = {
    'Cookie':"_uab_collina=172562103272506341622881; JSESSIONID=0BE2D4C431DDD4B0A5CDFA9E9193F0C4; BIGipServerotn=4141285642.24610.0000; BIGipServerpassport=937951498.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5E7F%u5DDE%2CGZQ; _jc_save_fromDate=2024-09-06; _jc_save_toDate=2024-09-06; _jc_save_wfdc_flag=dc",
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}
# 发送请请求
response = requests.get(url = url,headers = headers)
# 获取相应数据 response.json() 获取的响应json数据（必须完整的json数据格式）

# 解析数据 json_data 字典数据
json_data = response.json()
# 实例化对象
tb = PrettyTable()

# 设置字段名
tb.field_names = [
    '序号',
    '车次',
    '出发时间',
    '到达时间',
    '耗时',
    '特等座',
    '一等',
    '二等',
    '软卧',
    '硬卧',
    '硬座',
    '无座',
]
# 设置序号
page = 1
result = json_data['data']['result']

# for循环遍历，提取列表里面的元素
for i in result:

    # 字符串分割 -> index列表
    index = i.split('|')
    num = index[3]  # 车次
    start_time = index[8]   # 出发时间
    end_time = index[9]  # 到达时间
    use_time = index[10]    # 耗时
    topGrade = index[32]    # 特等座
    first_class = index[31]     # 一等
    second_class = index[30]    # 二等
    hard_sleeper = index[28]    # 硬卧
    hard_seat = index[29]  # 硬座
    no_seat = index[26]  # 无座
    soft_sleeper = index[23]  # 软卧

    dit = {
        '车次': num,
        '出发时间':start_time,
        '到达时间': end_time,
        '耗时': use_time,
        '特等座': topGrade,
        '一等': first_class,
        '二等': second_class,
        '软卧': soft_sleeper,
        '硬卧': hard_sleeper,
        '硬座': hard_seat,
        '无座': no_seat,
    }
    # 添加字段内容
    tb.add_row([
        page,
        num,
        start_time,
        end_time,
        use_time,
        topGrade,
        first_class,
        second_class,
        soft_sleeper,
        hard_sleeper,
        hard_seat,
        no_seat,
    ])
    page += 1
print(tb)