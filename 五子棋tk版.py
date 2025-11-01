# -*- coding: utf-8 -*-
"""
一个使用 tkinter 编写的图形化五子棋游戏。
"""

import tkinter as tk
from tkinter import messagebox

# --- 常量定义 ---

BOARD_SIZE = 15  # 棋盘大小 (15x15)
CELL_SIZE = 40  # 每个格子的像素大小
PADDING = 20  # 棋盘边缘的空白
DOT_RADIUS = 3  # 棋盘上"天元"和"星"的标记点半径

# 棋子半径
PIECE_RADIUS = CELL_SIZE // 2 - 4

# 颜色
COLOR_BOARD = "#DBA87B"  # 棋盘背景色 (米黄色)
COLOR_LINE = "#000000"  # 棋盘线条颜色
COLOR_BLACK = "#000000"  # 黑棋
COLOR_WHITE = "#FFFFFF"  # 白棋

# 玩家标识
PLAYER_BLACK = "●"
PLAYER_WHITE = "○"
EMPTY_SLOT = "+"


class GobangApp:
    def __init__(self, root):
        """
        初始化游戏应用
        """
        self.root = root
        self.root.title("五子棋 (Gobang)")
        self.root.resizable(False, False)  # 不允许改变窗口大小

        # 计算 Canvas 的总大小
        canvas_dim = CELL_SIZE * (BOARD_SIZE - 1) + PADDING * 2

        # --- 游戏状态变量 ---
        self.board_logic = []  # 存储棋盘逻辑的二维列表
        self.current_player = PLAYER_BLACK
        self.game_over = False
        self.move_count = 0

        # --- 创建界面组件 ---

        # 顶部框架 (用于状态标签和按钮)
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # 状态标签
        self.status_label = tk.Label(
            top_frame, text="黑棋 (●) 的回合", font=("Arial", 16)
        )
        self.status_label.pack(side=tk.LEFT, padx=20)

        # "新游戏" 按钮
        self.reset_button = tk.Button(
            top_frame, text="新游戏", font=("Arial", 14), command=self.reset_game
        )
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        # 棋盘 Canvas
        self.canvas = tk.Canvas(
            self.root, width=canvas_dim, height=canvas_dim, bg=COLOR_BOARD
        )
        self.canvas.pack(padx=10, pady=(0, 10))

        # 绑定鼠标点击事件
        self.canvas.bind("<Button-1>", self.on_click)

        # 启动新游戏
        self.reset_game()

    def draw_board(self):
        """
        在 Canvas 上绘制棋盘网格和标记点
        """
        # 清除旧的网格（如果有的话）
        self.canvas.delete("grid_line")
        self.canvas.delete("dot")

        max_coord = CELL_SIZE * (BOARD_SIZE - 1) + PADDING

        # 绘制 15 条横线和 15 条竖线
        for i in range(BOARD_SIZE):
            pos = i * CELL_SIZE + PADDING

            # (x1, y1, x2, y2)
            # 横线
            self.canvas.create_line(
                PADDING, pos, max_coord, pos, fill=COLOR_LINE, tags="grid_line"
            )
            # 竖线
            self.canvas.create_line(
                pos, PADDING, pos, max_coord, fill=COLOR_LINE, tags="grid_line"
            )

        # 绘制标记点 (天元和星)
        star_points = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]  # 四个角  # 天元

        for r, c in star_points:
            x = PADDING + c * CELL_SIZE
            y = PADDING + r * CELL_SIZE
            self.canvas.create_oval(
                x - DOT_RADIUS,
                y - DOT_RADIUS,
                x + DOT_RADIUS,
                y + DOT_RADIUS,
                fill=COLOR_LINE,
                tags="dot",
            )

    def reset_game(self):
        """
        重置游戏状态，开始新游戏
        """
        # 1. 重置逻辑棋盘
        self.board_logic = [
            [EMPTY_SLOT for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]

        # 2. 重置状态变量
        self.current_player = PLAYER_BLACK
        self.game_over = False
        self.move_count = 0

        # 3. 更新状态标签
        self.status_label.config(text="黑棋 (●) 的回合")

        # 4. 清空 Canvas 上的棋子
        self.canvas.delete("piece")

        # 5. 重新绘制棋盘网格
        self.draw_board()

    def on_click(self, event):
        """
        处理鼠标点击事件
        """
        if self.game_over:
            return  # 游戏已结束，不再响应点击

        # 1. 将像素坐标转换为网格坐标 (row, col)
        # 我们需要找到最近的交叉点
        col = round((event.x - PADDING) / CELL_SIZE)
        row = round((event.y - PADDING) / CELL_SIZE)

        # 2. 检查坐标是否有效
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return  # 点击在棋盘外

        # 3. 检查该位置是否已被占用
        if self.board_logic[row][col] != EMPTY_SLOT:
            # print("该位置已有棋子") # 可以在控制台输出提示
            return

        # 4. 执行落子
        self.make_move(row, col)

    def make_move(self, row, col):
        """
        执行一步棋，包括绘制棋子、更新逻辑、检查胜负
        """
        # 1. 在逻辑棋盘上落子
        self.board_logic[row][col] = self.current_player
        self.move_count += 1

        # 2. 在 Canvas 上绘制棋子
        self.draw_piece(row, col, self.current_player)

        # 3. 检查是否获胜
        if self.check_win(row, col, self.current_player):
            self.game_over = True
            winner_name = (
                "黑棋 (●)" if self.current_player == PLAYER_BLACK else "白棋 (○)"
            )
            self.status_label.config(text=f"游戏结束！{winner_name} 获胜！")
            messagebox.showinfo("游戏结束", f"恭喜 {winner_name} 获胜！")

        # 4. 检查是否平局
        elif self.move_count == BOARD_SIZE * BOARD_SIZE:
            self.game_over = True
            self.status_label.config(text="游戏结束！平局。")
            messagebox.showinfo("游戏结束", "平局！")

        # 5. 切换玩家 (如果游戏未结束)
        else:
            if self.current_player == PLAYER_BLACK:
                self.current_player = PLAYER_WHITE
                self.status_label.config(text="白棋 (○) 的回合")
            else:
                self.current_player = PLAYER_BLACK
                self.status_label.config(text="黑棋 (●) 的回合")

    def draw_piece(self, row, col, player):
        """
        在指定网格位置 (row, col) 绘制一个棋子
        """
        # 计算棋子中心的像素坐标
        center_x = PADDING + col * CELL_SIZE
        center_y = PADDING + row * CELL_SIZE

        # 计算棋子的边界 (x0, y0, x1, y1)
        x0 = center_x - PIECE_RADIUS
        y0 = center_y - PIECE_RADIUS
        x1 = center_x + PIECE_RADIUS
        y1 = center_y + PIECE_RADIUS

        # 选择颜色
        color = COLOR_BLACK if player == PLAYER_BLACK else COLOR_WHITE
        outline_color = COLOR_BLACK  # 无论黑白，都给个黑边，白色棋子才明显

        # 绘制棋子，并添加 "piece" 标签以便将来清除
        self.canvas.create_oval(
            x0, y0, x1, y1, fill=color, outline=outline_color, width=1, tags="piece"
        )

    def check_win(self, r, c, player):
        """
        检查玩家在 (r, c) 落子后是否获胜 (逻辑与命令行版相同)
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 水平, 垂直, \, /

        for dr, dc in directions:
            count = 1  # 计入射刚刚下的这颗子

            # 向正方向检查
            for i in range(1, 5):
                nr, nc = r + dr * i, c + dc * i
                if (
                    0 <= nr < BOARD_SIZE
                    and 0 <= nc < BOARD_SIZE
                    and self.board_logic[nr][nc] == player
                ):
                    count += 1
                else:
                    break

            # 向反方向检查
            for i in range(1, 5):
                nr, nc = r - dr * i, c - dc * i
                if (
                    0 <= nr < BOARD_SIZE
                    and 0 <= nc < BOARD_SIZE
                    and self.board_logic[nr][nc] == player
                ):
                    count += 1
                else:
                    break

            # 检查是否达到5个
            if count >= 5:
                return True

        return False


# --- 程序主入口 ---
if __name__ == "__main__":
    main_root = tk.Tk()
    app = GobangApp(main_root)
    main_root.mainloop()
