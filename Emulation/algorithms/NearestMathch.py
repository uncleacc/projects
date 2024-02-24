from tqdm import tqdm
import Utils
import Constant


def NearestMathch_algorithm():
    stream = Constant.stream
    totalRequest = 0
    totalHit = 0
    for i in tqdm(range(len(stream)), desc = "NearestMatch", unit = "i"):
        data = stream.read()
        content = data[1]
        user = Utils.getUser(content.userId)
        if user.request(content):
            totalHit += 1
        totalRequest += 1

    print("NearestMatch:")
    print(f"总请求数量：{totalRequest}")
    print(f"总命中数量：{totalHit}")
    print(f"命中率：{totalHit / totalRequest}")