import random
from collections import Counter
import matplotlib.pyplot as plt
import Utils
import Constant
import numpy as np
from tqdm import tqdm


def thompson_sampling(data_set, cachesize, lastBeta):
    """
    TS算法
    对于不同的缓存大小，执行TS时，得到的beta分布的参数不同，所以对于每个缓存大小都要跑一边TS
    :param data_set: 数据集
    :param cachesize: 缓存大小
    :return:
    """
    # 初始化beta分布系数为上次运行结束的状态
    music_in_dataset = [ct.song for ct in data_set]
    beta_hits_losses = {}
    for music_name in music_in_dataset:
        if lastBeta.get(music_name) is not None:
            beta_hits_losses[music_name] = lastBeta[music_name]
        else:
            beta_hits_losses[music_name] = [1, 1]
    # 初始化推荐音乐列表
    recommend_musics = []

    for epoch in range(100):
        # 初始化推荐音乐
        recommend_musics = []
        # 训练回合
        for idx in range(Constant.USERNUMBER):
            prob_musics = []
            # 每一个音乐的概率，将其合并为[music_name, prob] append到prob_musics
            for music_name in music_in_dataset:
                prob_musics.append([music_name, random.betavariate(beta_hits_losses[music_name][0],
                                                                 beta_hits_losses[music_name][1])])
            # 选取概率最大的作为推荐列表
            prob_musics.sort(key=lambda x: x[1], reverse=True)
            # print(prob_musics)
            recommend_music_i = []
            for i in range(min(len(music_in_dataset), cachesize)):
                # 设置一个阈值，概率太低就不要推荐了
                if prob_musics[i][1] > 0.4:
                    recommend_music_i.append(prob_musics[i])
            recommend_musics.append(recommend_music_i)

        # 汇总所有用户，计算平均概率，并得到前cachesize个音乐
        recommend_musics = Utils.count_top_items(cachesize, recommend_musics)
        # 更新beta参数
        # 得到dataset中请求的音乐
        musics_request = [ct.song for ct in data_set]
        count = Counter(musics_request)
        # 对于所有的音乐，根据命中次数来调整hits值和losses值
        # 将所有音乐的命中次数归一化再乘以5
        for music_name in recommend_musics:

            if music_name in count.keys():
                beta_hits_losses[music_name][0] += round(count[music_name]/max(count.values())*5)
            else:
                beta_hits_losses[music_name][1] += 1

    return recommend_musics, beta_hits_losses


def Thompson_Sampling_Run():
    window = 128 # 滑动窗口大小，每一次窗口移动，都会进行一次预测
    lastBeta = {}
    total = 0
    hit = 0
    cor_predict = 0
    predict_list = []
    recommand = []
    for i in tqdm(range(Constant.stream.length()), desc = "Thompson_Sampling", unit = "i"):
        content = Constant.stream[i][1]
        user = Utils.getUser(content.userId)
        if content.song in recommand:
            cor_predict += 1
        if user.request(content):
            hit += 1
        total += 1
        # 滑动窗口
        if (i + 1) % window == 0:
            # recommand是一个列表，列表中的每个元素是一个元组，元组的第一个元素是歌曲id，第二个元素是歌曲的概率            
            predict_list.append(cor_predict / window)

            dataWindow = Constant.stream[i + 1 - window : i]
            contents = [item[1] for item in dataWindow]

            recommand, beta_hits_losses = thompson_sampling(contents, Constant.CACHECAPACITY // 2, lastBeta)

            lastBeta = beta_hits_losses
            cor_predict = 0

            bs = user.server
            for j in range(len(recommand)):
                bs.add(recommand[j])
    
    print("Thompson_Sampling算法：")
    print(f"总请求数量：{total}")
    print(f"总命中数量：{hit}")
    print(f"缓存命中率：{hit / total}")
    print(f"预测命中率：{sum(predict_list) / len(predict_list)}")