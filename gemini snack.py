import pygame
import sys
import random
import time

# 检查 pygame 初始化是否成功
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f"(!) 字体初始化失败: {check_errors[1]} 个错误")
    sys.exit(-1)
else:
    print("(+) Pygame 初始化成功!")

# --- 游戏设置 ---

# 1. 屏幕尺寸
screen_width = 720
screen_height = 480

# 2. 颜色 (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)  # 游戏结束
GREEN = pygame.Color(0, 255, 0)  # 蛇
BLUE = pygame.Color(0, 0, 255)  # 食物

# 3. 游戏控制器
# Pygame 使用一个时钟来控制游戏的帧率 (FPS)
fps_controller = pygame.time.Clock()
game_speed = 15  # 初始速度

# 4. 游戏窗口
pygame.display.set_caption("Python 贪吃蛇")
game_window = pygame.display.set_mode((screen_width, screen_height))

# --- 游戏变量 ---

# 蛇的初始位置和大小
# 我们将游戏视为一个网格，蛇的每个方块大小为 10x10 像素
snake_pos = [100, 50]  # 蛇头的 x, y 坐标
snake_body = [[100, 50], [90, 50], [80, 50]]  # 蛇头  # 蛇身  # 蛇尾
block_size = 10

# 食物
food_pos = [
    random.randrange(1, (screen_width // block_size)) * block_size,
    random.randrange(1, (screen_height // block_size)) * block_size,
]
food_spawn = True

# 初始方向
direction = "RIGHT"
change_to = direction

# 分数
score = 0

# --- 核心功能函数 ---


def game_over():
    """
    游戏结束函数
    """
    my_font = pygame.font.SysFont("Arial", 50)  # 使用系统字体 'Arial'
    game_over_surface = my_font.render("GAME OVER!", True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)

    game_window.fill(BLACK)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0)  # 0 表示显示最终分数
    pygame.display.flip()

    # 等待 2 秒后退出
    time.sleep(2)
    pygame.quit()
    sys.exit()


def show_score(choice):
    """
    显示分数
    choice=1: 显示游戏中的分数
    choice=0: 显示游戏结束时的分数
    """
    score_font = pygame.font.SysFont("Arial", 24)
    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_surface.get_rect()

    if choice == 1:
        # 显示在左上角
        score_rect.midtop = (screen_width / 10, 15)
    else:
        # 显示在屏幕中间
        score_rect.midtop = (screen_width / 2, screen_height / 1.25)

    game_window.blit(score_surface, score_rect)


# --- 游戏主循环 ---

while True:
    # 1. 处理用户输入（事件）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 检查按键
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                change_to = "UP"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                change_to = "DOWN"
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                change_to = "RIGHT"
            # 按 'ESC' 退出
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # 2. 验证方向（防止蛇 180 度掉头）
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # 3. 更新蛇的位置
    if direction == "UP":
        snake_pos[1] -= block_size
    if direction == "DOWN":
        snake_pos[1] += block_size
    if direction == "LEFT":
        snake_pos[0] -= block_size
    if direction == "RIGHT":
        snake_pos[0] += block_size

    # 4. 蛇的身体增长机制
    # (1) 在蛇头的新位置插入一个方块
    snake_body.insert(0, list(snake_pos))

    # (2) 检查是否吃到食物
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False  # 需要生成新食物
    else:
        # 如果没吃到食物，就移除蛇尾的方块（保持长度不变）
        snake_body.pop()

    # 5. 生成新食物
    if not food_spawn:
        food_pos = [
            random.randrange(1, (screen_width // block_size)) * block_size,
            random.randrange(1, (screen_height // block_size)) * block_size,
        ]
    food_spawn = True

    # 6. 绘制游戏界面
    game_window.fill(BLACK)  # 黑色背景

    # 绘制蛇
    for pos in snake_body:
        pygame.draw.rect(
            game_window, GREEN, pygame.Rect(pos[0], pos[1], block_size, block_size)
        )

    # 绘制食物
    pygame.draw.rect(
        game_window, BLUE, pygame.Rect(food_pos[0], food_pos[1], block_size, block_size)
    )

    # 7. 游戏结束条件
    # (1) 撞到墙壁
    if snake_pos[0] < 0 or snake_pos[0] > screen_width - block_size:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > screen_height - block_size:
        game_over()

    # (2) 撞到自己
    # 检查蛇头是否碰到了身体的任何一个部分 (除了蛇头自己)
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # 8. 显示分数
    show_score(1)

    # 9. 刷新屏幕
    pygame.display.update()

    # 10. 控制游戏速度
    fps_controller.tick(game_speed)
