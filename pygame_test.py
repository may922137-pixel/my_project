import pygame
import random
import sys

# 1. 初始化 Pygame
pygame.init()

# 2. 屏幕设置
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
try:
    # 尝试使用可缩放窗口，这在 VNC/X11 环境中兼容性更好
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
except pygame.error:
    print("无法设置可缩放模式，使用普通模式")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Pygame 性能测试 (Termux)")

# 3. 性能计数器
clock = pygame.time.Clock()
try:
    font = pygame.font.SysFont(None, 30)
except:
    print("无法加载系统字体，FPS 将无法显示")
    font = None


# 4. 小球类 (核心)
class Ball:
    def __init__(self, x, y, radius, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy

        # 关键测试点：创建一个带 Alpha 透明度的 surface
        # (R, G, B, Alpha)，Alpha 100-200 之间为半透明
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(100, 200),
        )

        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, color, (radius, radius), radius)

    def update(self, width, height):
        self.x += self.dx
        self.y += self.dy

        # 碰撞检测
        if self.x <= self.radius or self.x >= width - self.radius:
            self.dx *= -1
        if self.y <= self.radius or self.y >= height - self.radius:
            self.dy *= -1

    def draw(self, target_screen):
        # 绘制这个半透明的 surface，这是最耗费CPU的操作
        target_screen.blit(self.surface, (self.x - self.radius, self.y - self.radius))


# 5. 初始化小球列表
balls = []
INITIAL_BALL_COUNT = 50  # 初始小球数量


def create_random_ball(width, height):
    radius = random.randint(10, 25)
    x = random.randint(radius, width - radius)
    y = random.randint(radius, height - radius)
    dx = random.uniform(-2, 2)
    dy = random.uniform(-2, 2)
    return Ball(x, y, radius, dx, dy)


# 获取当前窗口大小
current_width, current_height = screen.get_size()
for _ in range(INITIAL_BALL_COUNT):
    balls.append(create_random_ball(current_width, current_height))

# 6. 游戏主循环
running = True
while running:
    # 获取当前窗口大小（适配窗口缩放）
    current_width, current_height = screen.get_size()

    # --- 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 每次点击，增加 10 个小球
            for _ in range(10):
                balls.append(create_random_ball(current_width, current_height))

    # --- 逻辑更新 ---
    for ball in balls:
        ball.update(current_width, current_height)

    # --- 渲染(绘制) ---
    screen.fill((0, 0, 0))  # 填充黑色背景

    for ball in balls:
        ball.draw(screen)  # 绘制所有小球

    # 绘制 FPS 和小球数量
    if font:
        fps_text = f"FPS: {int(clock.get_fps())}"
        ball_count_text = f"Balls: {len(balls)}"

        fps_surface = font.render(fps_text, True, (255, 255, 255))
        ball_count_surface = font.render(ball_count_text, True, (255, 255, 255))

        screen.blit(fps_surface, (10, 10))
        screen.blit(ball_count_surface, (10, 40))

    # --- 刷新屏幕 ---
    pygame.display.flip()

    # --- 控制帧率 ---
    # 我们将其限制在 60 FPS，看看它能否保持
    clock.tick(60)

# 7. 退出
pygame.quit()
sys.exit()
