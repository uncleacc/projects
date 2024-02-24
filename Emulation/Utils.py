import time
import User
from Constant import *
from collections import Counter
import numpy as np


class LogTime:
    """
    Time used help.
    You can use count_time() in for-loop to count how many times have looped.
    Call finish() when your for-loop work finish.
    WARNING: Consider in multi-for-loop, call count_time() too many times will slow the speed down.
            So, use count_time() in the most outer for-loop are preferred.
    """

    def __init__(self, print_step=20000, words=''):
        """
        How many steps to print a progress log.
        :param print_step: steps to print a progress log.
        :param words: help massage
        """
        self.proccess_count = 0
        self.PRINT_STEP = print_step
        # record the calculate time has spent.
        self.start_time = time.time()
        self.words = words
        self.total_time = 0.0

    def count_time(self):
        """
        Called in for-loop.
        :return:
        """
        # log steps and times.
        if self.proccess_count % self.PRINT_STEP == 0:
            curr_time = time.time()
            print(self.words + ' steps(%d), %.2f seconds have spent..' % (
                self.proccess_count, curr_time - self.start_time))
        self.proccess_count += 1

    def finish(self):
        """
        Work finished! Congratulations!
        :return:
        """
        print('total %s step number is %d' % (self.words, self.get_curr_step()))
        print('total %.2f seconds have spent\n' % self.get_total_time())

    def get_curr_step(self):
        return self.proccess_count

    def get_total_time(self):
        return time.time() - self.start_time
    
def getUser(userid):
    for user in users:
        if(user.id == userid):
            return user
    return None

def hashProcess(data):
    from Constant import hash2name, name2hash
    for i in range(len(data)):
        hash2name[hash(data[i])] = data[i]
        name2hash[data[i]] = hash(data[i])


def count_top_items(num, items):
    """
    在items中选择出现频次最高的num个
    :param num: 选择出现频次最高的num个
    :param items: 输入的items为二阶列表。例如[[1,2,3],[12,3,5]]
    :return:
    """
    # 把二阶列表转换为一阶列表
    oneL = []
    for item in items:
        oneL.extend(item)
    # 找到观看历史中次数最多的前num部电影
    # count = Counter(oneL)
    
    # top_items = np.array(count.most_common(num))[:, 0]
        
    avg = calculate_average_probability(oneL)
    top_items = sorted(avg.items(), key=lambda x: x[1], reverse=True)[:num]
    top_items = np.array(top_items)[:, 0]
    return top_items

def calculate_average_probability(recommendations):
    """
    Calculate the average request probability for each music in the recommendation list.
    :param recommendations: List of tuples containing music name and request probability.
    :return: Dictionary with music name as key and average request probability as value.
    """
    music_probabilities = {}
    for music, probability in recommendations:
        if music in music_probabilities:
            music_probabilities[music].append(probability)
        else:
            music_probabilities[music] = [probability]

    average_probabilities = {}
    for music, probabilities in music_probabilities.items():
        average_probabilities[music] = sum(probabilities) / len(probabilities)

    return average_probabilities

