'''
'''
import FileOperation
import sys


class DataStream:
    '''
    成员变量：
    - stream: 请求的数据流[time, content]
    - 
    '''
    stream: list
    def __init__(self, file_name = "", limit = sys.maxsize) -> None:
        self.stream = []
        if file_name:
            self.readDataStream(file_name, limit)
    
    def readDataStream(self, file_name, limit = sys.maxsize):
        '''
        读取数据流
        '''
        self.stream = FileOperation.readDataStream(file_name, limit)
    
    def read(self):
        '''
        返回一个请求
        '''
        if(len(self.stream) == 0):
            return None
        return self.stream.pop(0)

    def empty(self):
        '''
        判断数据流是否为空
        '''
        return len(self.stream) == 0

    def __len__(self):
        return len(self.stream)
    
    def __getitem__(self, key):
        return self.stream[key]
    
    def length(self):
        return len(self.stream)
    
    def data(self):
        return self.stream
