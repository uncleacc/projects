import BaseStation
from Constant import *
from tqdm import tqdm
from DataStream import DataStream


def displayBindInfo():
    '''
    展示基站绑定的用户id
    '''
    for base in baseStations:
        print(base.id)
        base.printUsers()
        print('-----------------------------')

def calcSongNum(stream):
    '''
    计算所有用户请求的歌曲种类数量
    '''
    songSet = set()
    for i in range(len(stream)):
        data = stream.read()
        content = data[1]
        songSet.add(content.author + content.song)
        if i % 10000 == 0:
            print(f'{i} songs')

    return len(songSet)

def display_stream(stream):
    '''
    展示数据流
    '''
    for i in range(len(stream)):
        data = stream.read()
        print(data[0], data[1].song)