"""
File: Environment.py
Author: Doraemon
Description: 初始化边缘缓存的环境
"""
from BaseStation import *
from User import *
from DataStream import DataStream
import DrawGraph
import Debug
import FileOperation
import random
import math
import Utils
import Constant
from tqdm import tqdm
from algorithms.NearestMathch import NearestMathch_algorithm
from algorithms.Thompson_Sampling import Thompson_Sampling_Run
from algorithms.LSTM import LSTM_Run


# 随机分布用户
def generate_random_points_in_circle(RADIUS, n):
    points = []
    for _ in range(n):
        # 生成随机角度
        theta = random.uniform(0, 2 * math.pi)
        # 生成随机半径
        r = math.sqrt(random.uniform(0, 1)) * RADIUS
        # 转换为直角坐标系
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y))

    return points

def initEnvironment():
    # 基站
    id = 0
    for x, y in BASECOORDINATE:
        baseStations.append(BaseStation(id, x, y))
        id += 1
    # 用户
    userIdList = []
    with open(Constant.USERID_PATH) as file:
        lines = file.readlines()
        for user_id in lines:
            user_id = user_id.strip()
            userIdList.append(user_id)
    
    # random_points = generate_random_points_in_circle(RADIUS, USERNUMBER)
    # FileOperation.writeUserInfo(random_points, userIdList)
    random_points = FileOperation.readUserInfo(Constant.USER_COORDINATE_PATH)

    for i in range(USERNUMBER):
        users.append(User(userIdList[i], random_points[i][0], random_points[i][1]))
        users[i].BindBaseStation() # 绑定到最近的基站

    # Constant.stream = DataStream(Constant.DATASET_PATH)
    Constant.stream = DataStream(Constant.DATASET_PATH, 10000)

    # Debug.display_stream(Constant.stream)
    # Debug.displayBindInfo()
    # print(Debug.calcSongNum(Constant.stream))
    # DrawGraph.display(random_points, BASECOORDINATE)

        
def start():
    # Thompson_Sampling_Run()
    # NearestMathch_algorithm()
    LSTM_Run()


if __name__ == '__main__':
    initEnvironment()
    start()

