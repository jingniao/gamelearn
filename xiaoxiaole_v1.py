"""
文字类消消乐
先用文字版的将游戏逻辑理清

游戏逻辑
1，生成一个10 * 10的矩阵，每个节点随机从1-5中选择一个，填充，表示不同颜色
2，输入一个坐标(x,y)，搜索xy周围是否有相同颜色，找到相同颜色，找出所有，记录坐标
    按照给出的坐标，删除指定坐标
    返回修改后的分布图
"""
import random
from collections import deque
import copy


class Xiaoxiaole:
    def __init__(self):
        # 生成棋盘
        self.chess = [[random.randint(1, 5) for i in range(10)] for i in range(10)]
        self.sources = 0

    def get_chess(self):
        # 获取当前棋盘
        return copy.deepcopy(self.chess)

    def can_continue(self):
        for x,line in enumerate(self.chess):
            for y,_ in enumerate(line):
                if self.search(x,y):
                    return True
        return False


    def get_source(self):
        return self.sources

    def search(self, x, y):
        # 获取x y 节点附近的相同节点坐标，如果没有相同的返回None
        point_value = self.chess[x][y]
        out = set()
        out.add((x, y))
        deq = deque()
        deq.append((x, y))

        while len(deq):
            now = deq.popleft()
            neighbors = [(now[0] - 1, now[1]), (now[0] + 1, now[1]), (now[0], now[1] - 1),
                         (now[0], now[1] + 1)]
            chess_len = len(self.chess)
            for neighbor in neighbors:
                if neighbor in out:
                    continue
                if neighbor[0] < 0 or neighbor[0] >= chess_len:
                    continue
                if neighbor[1] < 0 or neighbor[1] >= len(self.chess[neighbor[0]]):
                    continue
                if self.chess[neighbor[0]][neighbor[1]] == point_value:
                    deq.append(neighbor)
                    out.add(neighbor)
        if len(out) > 1:
            return out
        else:
            return None

    def client(self, x, y):
        # 点击坐标点，如果有消除动作，则返回True，如果没有消除动作返回False

        # 判断x y是否在chess中
        if len(self.chess) <= x:
            return False
        if len(self.chess[x]) <= y:
            return False

        # 搜索相邻的节点，返回set
        to_del = self.search(x, y)
        if not to_del:
            return False

        # 更新分数
        self.sources += pow(len(to_del), 2) * 5

        # 删除节点
        to_del = sorted(to_del, key=lambda x: x[1], reverse=True)
        for point in to_del:
            del self.chess[point[0]][point[1]]

        # 删除空列
        for index in range(len(self.chess) - 1, -1, -1):
            if not self.chess[index]:
                del self.chess[index]
        return True


def out_line(chess):
    # 将chess左旋90度输出
    for line in chess:
        line.extend([9] * (10 - len(line)))
    chess = [list(x) for x in zip(*chess)]
    for line in reversed(chess):
        line = [str(x) for x in line]
        out = '  '.join(line).replace('9', ' ')
        print(out)


xiaoxiaole = Xiaoxiaole()
out_line(xiaoxiaole.get_chess())

while xiaoxiaole.can_continue():
    choice = input()
    try:
        inp = choice.split()
        if len(inp) != 2:
            print("非法输入")
            continue
        x = int(inp[0])
        y = int(inp[1])
        if x is not None and y is not None and x >= 0 and x <= 9 and y >= 0 and y <= 9:
            print("获得坐标点: {0} {1}".format(x, y))
        else:
            print("非法输入")
            continue
    except:
        continue
    res = xiaoxiaole.client(x, y)
    if res:
        print("当前分数：{0}".format(xiaoxiaole.get_source()))
        out_line(xiaoxiaole.get_chess())
    else:
        print("无效操作")

print("游戏结束，最终分数为：{0}".format(xiaoxiaole.get_source()))
