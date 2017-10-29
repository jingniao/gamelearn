import random
from collections import deque

import pygame
from pygame.locals import MOUSEBUTTONUP, QUIT

Color = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 0, 255)
}


class Box(pygame.sprite.Sprite):
    def __init__(self, color, position):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.rect = self.image.fill(color=color)
        self.rect.topleft = position
        self.change_x = 0
        self.change_y = 0

    def update(self):
        if self.change_x:
            self.rect.x -= self.change_x * 40
            self.change_x = 0
        if self.change_y:
            self.rect.y += self.change_y * 40
            self.change_y = 0


class Xiaoxiaole:
    def __init__(self, group):
        # 生成棋盘，传入参数为精灵group
        self.sorces = 0
        self.chess = []
        self.group = group

        for x in range(10):
            x_line = []
            for y in range(10):
                pos = (40 * x, 40 * (9 - y))
                color = random.randint(1, 5)
                box = Box(Color[color], pos)
                group.add(box)
                x_line.append((color, box))
            self.chess.append(x_line)

    def can_continue(self):
        for x, line in enumerate(self.chess):
            for y, _ in enumerate(line):
                if self.search(x, y):
                    return True
        return False

    def get_sorce(self):
        return self.sorces

    def search(self, x, y):
        # 获取x y 节点附近的相同节点坐标，如果没有相同的返回None
        point_value = self.chess[x][y][0]
        out = set()
        out.add((x, y))
        deq = deque()
        deq.append((x, y))

        while len(deq):
            # 广度优先搜索
            now = deq.popleft()
            neighbors = [(now[0] - 1, now[1]), (now[0] + 1, now[1]),
                         (now[0], now[1] - 1), (now[0], now[1] + 1)]
            chess_len = len(self.chess)
            for neighbor in neighbors:
                if neighbor in out:
                    continue
                if neighbor[0] < 0 or neighbor[0] >= chess_len:
                    continue
                if neighbor[1] < 0 or neighbor[1] >= len(
                        self.chess[neighbor[0]]):
                    continue
                if self.chess[neighbor[0]][neighbor[1]][0] == point_value:
                    deq.append(neighbor)
                    out.add(neighbor)
        if len(out) > 1:
            return out
        else:
            return None

    def client(self, pos):
        # 点击坐标点，如果有消除动作，则返回True，如果没有消除动作返回False
        x = pos[0] // 40
        y = 9 - (pos[1] // 40)
        # self.group.remove(self.chess[x][y][1])

        # # 判断x y是否在chess中
        if len(self.chess) <= x:
            return False
        if len(self.chess[x]) <= y:
            return False

        # 搜索相邻的节点，返回set
        to_del_set = self.search(x, y)
        if not to_del_set:
            return False

        # 更新分数
        self.sorces += pow(len(to_del_set), 2) * 5

        # 删除节点
        #
        for point in to_del_set:
            self.group.remove(self.chess[point[0]][point[1]])
            #  处理在这个节点上部的移动标记
            for y_num in range(point[1], len(self.chess[point[0]])):
                self.chess[point[0]][y_num][1].change_y += 1

        to_del = sorted(to_del_set, key=lambda x: x[1], reverse=True)
        for point in to_del:
            del self.chess[point[0]][point[1]]

        # 删除空列
        for index, _ in enumerate(self.chess):
            if not self.chess[index]:
                # 将右侧所有节点向左移动一格
                for x_line in range(index + 1, len(self.chess)):
                    for y_line in range(0, len(self.chess[x_line])):
                        self.chess[x_line][y_line][1].change_x += 1
        for index in range(len(self.chess) - 1, -1, -1):
            if not self.chess[index]:
                del self.chess[index]
        return True


pygame.init()
screen = pygame.display.set_mode([400, 400])
bg = pygame.Surface([400, 400])
bg.fill([0, 0, 0])
group = pygame.sprite.Group()
xiaoxiaole = Xiaoxiaole(group)
group.draw(screen)
pygame.display.update()
clock = pygame.time.Clock()
pygame.event.set_allowed([QUIT, MOUSEBUTTONUP])

while True:
    clock.tick(30)
    event = pygame.event.poll()
    if event.type == QUIT:
        exit()
    elif event.type == MOUSEBUTTONUP:
        xiaoxiaole.client(event.pos)
        group.update()
        group.clear(screen, bg)
        group.draw(screen)
        pygame.display.update()

        if not xiaoxiaole.can_continue():
            group.empty()
            group.clear(screen, bg)
            group.draw(screen)
            my_font = pygame.font.SysFont("simsunnsimsun", 24)
            outline = '最终分数为：{0}'.format(xiaoxiaole.get_sorce())
            out = my_font.render(outline, False, (255, 255, 255))
            screen.blit(out, (20, 180))
            pygame.display.update()
