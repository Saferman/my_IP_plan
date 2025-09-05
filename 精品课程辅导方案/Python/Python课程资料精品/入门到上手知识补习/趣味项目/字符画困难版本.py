def olympic_rings():
    width, height = 50, 10  # 宽度和高度设置
    ring_centers = [(10, 3), (20, 3), (30, 3), (15, 5), (25, 5)]  # 五环中心坐标
    radius = 3  # 圆的半径

    # 初始化一个空的字符画矩阵
    canvas = [[' ' for _ in range(width)] for _ in range(height)]

    # 绘制每个圆环
    for cx, cy in ring_centers:
        for y in range(height):
            for x in range(width):
                # 使用圆的方程 (x - cx)^2 + (y - cy)^2 = r^2 来绘制圆形
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2 + 1 and (x - cx) ** 2 + (y - cy) ** 2 >= radius ** 2 - 1:
                    canvas[y][x] = 'O'

    # 打印字符画
    for row in canvas:
        print(''.join(row))

olympic_rings()
