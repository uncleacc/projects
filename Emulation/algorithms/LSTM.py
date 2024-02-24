import torch
import torch.nn as nn
from pandas import read_csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Constant
import Utils
from tqdm import tqdm
import FileOperation



def create_inout_sequences(input_data, tw):
    inout_seq = []
    L = len(input_data)
    for i in range(L-tw):
        train_seq = input_data[i:i+tw]
        train_label = input_data[i+tw:i+tw+1]
        inout_seq.append((train_seq ,train_label))
    return inout_seq

class LSTM(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=200, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM(input_size, hidden_layer_size)

        self.linear = nn.Linear(hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
                            torch.zeros(1,1,self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq) ,1, -1), self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-5:]

def train(model, bsid, baseStream, scaler, predict_window):
    # 删除所有参数
    torch.cuda.empty_cache()  # 清理GPU缓存

    # 基站的历史数据
    data = baseStream[bsid]
    train_data = np.array(data[-predict_window:]).reshape(-1, 1)
    
    train_data_normalized = scaler.fit_transform(train_data)
    train_data_normalized = torch.FloatTensor(train_data_normalized).view(-1)

    train_inout_seq = create_inout_sequences(train_data_normalized, predict_window)

    # 重新定义模型
    model[bsid] = LSTM()
    
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model[bsid].parameters(), lr=0.001)

    epochs = 200

    for i in range(epochs):
        for seq, labels in train_inout_seq:
            optimizer.zero_grad()
            model[bsid].hidden_cell = (torch.zeros(1, 1, model[bsid].hidden_layer_size),
                                torch.zeros(1, 1, model[bsid].hidden_layer_size))

            y_pred = model[bsid](seq)
            single_loss = loss_function(y_pred, labels)
            single_loss.backward()
            optimizer.step()

        # if i%25 == 1:
        #     print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')

def binary_search_first_larger(nums, val):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] >= val:
            if mid == 0 or nums[mid - 1] < val:
                return mid  # 找到第一个大于等于val的元素
            else:
                right = mid - 1
        else:
            left = mid + 1
    return -1  # 如果找不到大于等于val的元素，返回-1

def LSTM_Run():
    from Constant import name2hash, hash2name
    stream = np.array(Constant.stream.data())[:,1].reshape(-1)
    songList = list(set([ct.song for ct in stream])) # 去重+Hash
    Utils.hashProcess(songList)
    all_song_hash = []
    for key in hash2name.keys():
        all_song_hash.append(key)
    all_song_hash = sorted(all_song_hash)

    predict_window = 20 # 50个数据预测下一个数据
    training_size = 100 # 1000个数据训练一次
    baseStream = [[] for i in range(Constant.BASENUMBER)] # 基站的历史数据

    model = [LSTM() for i in range(Constant.BASENUMBER)] # 基站初始化LSTM模型

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    
    total = 0
    hit = 0
    predict_total = 0
    predict_success = 0

    for i in tqdm(range(len(Constant.stream)), desc = "LSTM", unit = "i"):
        content = Constant.stream.read()[1] # 请求内容

        user = Utils.getUser(content.userId)
        bs = user.server

        song_hash = name2hash[content.song]

        if len(baseStream[bs.id]) > training_size:
            hisData_normalized = scaler.fit_transform(np.array(baseStream[bs.id][-predict_window:]).reshape(-1, 1)) # 归一化
            hisData_normalized = torch.FloatTensor(hisData_normalized).view(-1)
            predict_songs = model[bs.id].forward(hisData_normalized) # 预测结果

            # 缓存预测结果
            for predict_song in predict_songs:
                # 二分从song_hash中找到最接近的歌曲
                idx = binary_search_first_larger(all_song_hash, predict_song)
                if idx == -1:
                    idx = len(all_song_hash) - 1
                mi = abs(all_song_hash[idx] - predict_song)
                predict_name = hash2name[all_song_hash[idx]]
                if idx - 1 > 0 and abs(all_song_hash[idx - 1] - predict_song) < mi:
                    mi = abs(all_song_hash[idx - 1] - predict_song)
                    predict_name = hash2name[all_song_hash[idx - 1]]
                if idx + 1 < len(all_song_hash) and abs(all_song_hash[idx + 1] - predict_song) < mi:
                    mi = abs(all_song_hash[idx + 1] - predict_song)
                    predict_name = hash2name[all_song_hash[idx + 1]]
                bs.add(predict_name)
                if predict_name == content.song:
                    predict_success += 1
            
            predict_total += 1
           


        baseStream[bs.id].append(song_hash)
        
        is_Hit = user.request(content)
        if(is_Hit):
            hit += 1
        total += 1

        # if len(baseStream[bs.id]) == 2 * training_size:
        #     FileOperation.writeBaseStream(baseStream[bs.id])
        #     exit(0)

        if len(baseStream[bs.id]) % training_size == 0:
            print(f"训练基站{bs.id}的LSTM模型")
            train(model, bs.id, baseStream, scaler, predict_window)
    
    print("LSTM算法：")
    print(f"总请求数量：{total}")
    print(f"总命中数量：{hit}")
    print(f"缓存命中率：{hit / total}")
    print(f"预测总次数：{predict_total}")
    print(f"预测成功次数：{predict_success}")
    print(f"预测成功率：{predict_success / predict_total}")

    