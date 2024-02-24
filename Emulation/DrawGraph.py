"""
File: DrawGraph.py
Author: Doraemon
Description: 封装绘图的函数
"""
import matplotlib.pyplot as plt
from Constant import *

def display(user_points, baseStation_points):
    plt.figure(figsize=(10, 8))
    # 绘制圆
    circle = plt.Circle((0, 0), RADIUS, color='b', fill=False, linestyle='dotted')
    plt.gca().add_patch(circle)

    # 提取 x 和 y 坐标
    user_x_coords, user_y_coords = zip(*user_points)
    base_x_coords, base_y_coords = zip(*baseStation_points)

    # 绘制随机点
    plt.scatter(user_x_coords, user_y_coords, color='r', marker='.')
    plt.scatter(base_x_coords, base_y_coords, color='black', marker='+')

    # 绘制基站的覆盖范围
    for base_x, base_y in BASECOORDINATE:
        plt.gca().add_patch(plt.Circle((base_x, base_y), BASERADIUS, color='g', fill=False, linestyle='solid'))

    # 设置坐标轴
    plt.axis('equal')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # 显示图形
    plt.show()
