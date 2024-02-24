"""
File: User.py
Author: Doraemon
Description: 用户类
"""
from BaseStation import *
from Constant import *


class User:
    '''
    成员变量：
    - id: 用户id
    - x: 坐标
    - y: 坐标
    - server: 绑定的基站
    
    方法：
    '''
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.server = None

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def BindBaseStation(self):
        min_dis = float('inf')
        bs = None
        for base in baseStations:
            if((base.x - self.x) ** 2 + (base.y - self.y) ** 2 < min_dis):
                min_dis = (base.x - self.x) ** 2 + (base.y - self.y) ** 2
                bs = base
        self.server = bs
        bs.addUser(self)
    
    def request(self, content):
        if Constant.DEBUG_ON:
            print(f'用户{self.id}请求{content.song}')
        if(content.song in self.server):
            if Constant.DEBUG_ON:
                print('命中')
            return True
        if Constant.DEBUG_ON:
            print('未命中')
        self.server.add(content.song)
        return False