import os
import sys
import Content
from tqdm import tqdm


def readUserInfo(file_name):
    '''
    读取用户id和坐标
    '''
    folder_path = 'E:\\MyProjects\\Experiment\\code\\cluster\\data\\UserCoordinate'

    # 过滤出只是文件的名字
    file_name = os.path.join(folder_path, file_name)

    # 读取文件
    with open(file_name, 'r') as file:
        lines = file.readlines()
        # 读取用户id和坐标，放到一个列表中，并按照用户id从小到大排序，返回排序后的坐标
        points = []
        for line in lines:
            line = line.strip()
            userid, x, y = line.split('\t')
            points.append((userid, float(x), float(y)))
        points.sort(key=lambda x: x[0])
        points = [point[1:] for point in points]
        return points


def writeUserInfo(points, userids):
    '''
    写入用户id和坐标到文件中，文件名自动选择最大的未出现的正整数
    '''
    folder_path = 'E:\\MyProjects\\Experiment\\code\\cluster\\data\\UserCoordinate'

    # 获取当前目录下所有文件和文件夹的名字
    all_files = os.listdir(folder_path)

    # 过滤出只是文件的名字
    file_names = [file for file in all_files if os.path.isfile(os.path.join(folder_path, file))]

    # 打印文件名
    preNum = -1
    writeFileName = None
    for file_name in file_names:
        file_name = file_name[:file_name.rfind('.')]
        if(int(file_name) != preNum + 1):
            writeFileName = str(preNum + 1) + ".txt"
            break
        preNum += 1

    if(writeFileName == None):
        writeFileName = str(preNum + 1) + ".txt"

    # 保存这组数据到文件中
    with open(os.path.join(folder_path, writeFileName), 'w') as file:
        for i in range(len(points)):
            x, y = points[i]
            file.write(f"{userids[i]}\t{x}\t{y}\n")


def writeBaseStream(stream):
    '''
    写入基站流
    '''
    from Constant import hash2name
    file_path = 'E:\\MyProjects\\Experiment\\dataset\\lastfm-dataset-1K\\Processed\\baseStationStream.txt'
    with open(file_path, 'w') as file:
        for song in stream:
            file.write(f"{song}|{hash2name[song]}\n")


def readDataStream(file_name, limit = sys.maxsize):
    '''
    读取数据流
    '''
    folder_path = 'E:\\MyProjects\\Experiment\\dataset\\lastfm-dataset-1K\\Processed'

    file_path = os.path.join(folder_path, file_name)

    contents = []

    # 获取文件总行数
    with open(file_path, 'r') as file:
        lines_list = list(file)
        total_lines = min(len(lines_list), limit)

    with tqdm(total=total_lines, desc="Reading", unit="line", disable=False) as pbar:
        # 读取文件
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):
                if idx >= limit:
                    break
                line = line.strip()
                user_id, time, author, song = line.split('\t')
                contents.append((time, Content.Content(song, author, user_id)))
                    # 更新进度条
                pbar.update(1)
        
    return contents