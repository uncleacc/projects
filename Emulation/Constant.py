# 文件路径
#=======================================
DATASET_PATH = 'E:/MyProjects/Experiment/dataset/lastfm-dataset-1K/Processed/filteredDatas.tsv'
USERID_PATH = 'E:/MyProjects/Experiment/dataset/lastfm-dataset-1K/Processed/most100Users.txt'
USER_COORDINATE_PATH = 'E:/MyProjects/Experiment/code/cluster/data/UserCoordinate/0.txt'
#=======================================


# DebugInfo
#=======================================
DEBUG_ON = False

#=======================================


# 数据结构
#=======================================
BASENUMBER = 13 # 基站数量
BASECOORDINATE = [
    (-300, 300),
    (0, 300),
    (300, 300),
    (-300, 0),
    (0, 0),
    (300, 0),
    (-300, -300),
    (0, -300),
    (300, -300),
    (-150, 150),
    (150, 150),
    (-150, -150),
    (150, -150)
    ] # 基站坐标
BASERADIUS = 200 # 基站的覆盖范围
CACHECAPACITY = 32 # 缓存容量
STORECOST = 0 # 存储成本
TRANSTIME = 1 # 传输速率

RADIUS = 500 # 仿真环境的半径
USERNUMBER = 100 # 用户数量


baseStations = [] # 基站集合
users = [] # 用户集合
stream = None # 数据流

__all__ = ['stream', 
           'baseStations', 
           'users', 
           'BASENUMBER', 
           'BASECOORDINATE', 
           'BASERADIUS', 
           'CACHECAPACITY', 
           'STORECOST', 
           'TRANSTIME', 
           'RADIUS', 
           'USERNUMBER'
           ]
#=======================================

name2hash = {}
hash2name = {}