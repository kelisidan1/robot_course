from tkinter import messagebox, Tk
import pygame
import sys

window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 50

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width-2, box_height-2))

    def calculate_cost(self, start, target):
        self.g_cost = abs(self.x - start.x) + abs(self.y - start.y)
        self.h_cost = abs(self.x - target.x) + abs(self.y - target.y)
        self.f_cost = self.g_cost + self.h_cost

    def set_neighbours(self, start, target):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])
        
        for neighbour in self.neighbours:
            neighbour.calculate_cost(start, target)


# 创建网格
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# 设置邻居
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours(grid[0][0], grid[0][0])


start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)


def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():
            # 退出窗口
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 鼠标控制
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # 绘制墙
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # 设置目标点
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # 启动算法
            if event.type == pygame.KEYDOWN and target_box_set:
                algorithm_choice = input("输入 1 使用Dijkstra 或 2 使用A*：")
                if algorithm_choice == "1":
                    begin_search = True
                elif algorithm_choice == "2":
                    begin_search = True
                    target_box.calculate_cost(start_box, target_box)

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("无解", "无法找到路径！")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))

                if box.start:
                    box.draw(window, (0, 200, 200))
                if box.wall:
                    box.draw(window, (10, 10, 10))
                if box.target:
                    box.draw(window, (200, 200, 0))

        pygame.display.flip()

main()
