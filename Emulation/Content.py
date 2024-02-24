"""
File: Content.py
Author: Doraemon
Description: 请求数据类
"""
class Content:
    '''
    成员变量：
    - song: 歌曲名称
    - author: 歌手名称
    - type: 歌曲类型
    - size: 歌曲大小, 暂时不考虑
    - deadline: 截止时间, 默认为0, 表示没有截止时间
    - userId: 来源
    
    方法：

    '''
    def __init__(self, song, author, userId):
        self.song = song
        self.author = author
        self.userId = userId
        self.deadline = 0

    def setSong(self, name):
        self.song = name
    
    def setAuthor(self, author):
        self.author = author
    
    def setType(self, type):
        self.type = type
    
    def setSize(self, size):
        self.size = size
    
    def setDeadline(self, deadline):
        self.deadline = deadline

    def setUserId(self, id):
        self.userId = id