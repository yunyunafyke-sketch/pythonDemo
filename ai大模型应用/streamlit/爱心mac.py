import tkinter as tk
import random
import math
import ctypes
import time
import sys
import os
import subprocess

WINDOW_W = 160
WINDOW_H = 38
NUM_WINDOWS = 96
HEART_STEP = 18
SCATTER_STEP = 26
HEART_FRAME_DELAY = 0.016
SCATTER_FRAME_DELAY = 0.012
HEART_PAUSE_MS = 1400

def get_screen_size():
    if sys.platform.startswith("win") and hasattr(ctypes, "windll"):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    temp_root = tk.Tk()
    temp_root.withdraw()
    temp_root.update_idletasks()
    screen_w = temp_root.winfo_screenwidth()
    screen_h = temp_root.winfo_screenheight()
    temp_root.destroy()
    return screen_w, screen_h


def activate_current_app():
    if sys.platform != "darwin":
        return

    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                (
                    'tell application "System Events" '
                    f'to set frontmost of the first process whose unix id is {os.getpid()} to true'
                ),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        pass


def generate_heart_points(num_points, window_width, window_height, screen_w, screen_h):
    t_list = [2 * math.pi * i / num_points for i in range(num_points)]
    raw = [
        (16 * math.sin(t) ** 3, 13 * math.cos(t) - 5 * math.cos(2 * t)
         - 2 * math.cos(3 * t) - math.cos(4 * t)) for t in t_list
    ]
    xs = [p[0] for p in raw]
    ys = [p[1] for p in raw]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    usable_w = screen_w - window_width
    usable_h = screen_h - window_height
    scale = min(usable_w / (max_x - min_x + 0.7), usable_h / (max_y - min_y + 0.8))
    heart_w = (max_x - min_x) * scale
    heart_h = (max_y - min_y) * scale
    base_x = (screen_w - heart_w) // 2
    base_y = (screen_h - heart_h) // 2
    mapped = []
    for x0, y0 in raw:
        nx = (x0 - min_x)
        ny = (y0 - min_y)
        px = int(base_x + nx * scale)
        py = int(base_y + heart_h - ny * scale)
        px = max(0, min(px, screen_w - window_width))
        py = max(0, min(py, screen_h - window_height))
        mapped.append((px, py))
    dedup = []
    seen = set()
    for p in mapped:
        if p not in seen:
            seen.add(p)
            dedup.append(p)
    return dedup[:num_points]


def generate_scatter_points(heart_points, window_width, window_height, screen_w, screen_h):
    max_x = max(0, screen_w - window_width)
    max_y = max(0, screen_h - window_height)
    center_x = sum(x for x, _ in heart_points) / len(heart_points)
    center_y = sum(y for _, y in heart_points) / len(heart_points)

    scatter_points = []
    for index, (x, y) in enumerate(heart_points):
        vx = x - center_x
        vy = y - center_y
        if abs(vx) < 1 and abs(vy) < 1:
            angle = 2 * math.pi * index / len(heart_points)
            vx = math.cos(angle)
            vy = math.sin(angle)

        scale_candidates = []
        if vx > 0:
            scale_candidates.append((max_x - x) / vx)
        elif vx < 0:
            scale_candidates.append((0 - x) / vx)

        if vy > 0:
            scale_candidates.append((max_y - y) / vy)
        elif vy < 0:
            scale_candidates.append((0 - y) / vy)

        scale = min(candidate for candidate in scale_candidates if candidate > 0)
        spread = random.uniform(0.82, 1.0)
        nx = int(round(x + vx * scale * spread))
        ny = int(round(y + vy * scale * spread))
        scatter_points.append((max(0, min(nx, max_x)), max(0, min(ny, max_y))))

    return scatter_points

tips = ['多喝水哦~ 邪恶面包', '保持微笑呀 邪恶面包', '每天都要元气满满 邪恶面包', '记得吃水果 邪恶面包', '保持好心情 邪恶面包',
        '好好爱自己 邪恶面包', '我想你了 邪恶面包', '梦想成真 邪恶面包', '期待下一次见面 邪恶面包',
        '天冷了，多穿衣服 邪恶面包', '愿所有烦恼都消失 邪恶面包', '不要熬夜 邪恶面包', '爱你哦~ 邪恶面包']
bg_colors = ['lightpink', 'skyblue', 'lightgreen', 'lavender', 'lightyellow',
            'plum', 'coral', 'bisque', 'aquamarine', 'mistyrose', 'honeydew']

if __name__ == "__main__":
    SCREEN_W, SCREEN_H = get_screen_size()
    margin_x = WINDOW_W // 2
    margin_y = WINDOW_H // 2
    points_start = []
    for _ in range(NUM_WINDOWS):
        x = random.randint(margin_x, SCREEN_W - WINDOW_W - margin_x)
        y = random.randint(margin_y, SCREEN_H - WINDOW_H - margin_y)
        points_start.append((x, y))
    points_heart = generate_heart_points(NUM_WINDOWS, WINDOW_W, WINDOW_H, SCREEN_W, SCREEN_H)
    if len(points_heart) < NUM_WINDOWS:
        points_heart += [points_heart[-1]] * (NUM_WINDOWS - len(points_heart))
    points_scatter = generate_scatter_points(points_heart, WINDOW_W, WINDOW_H, SCREEN_W, SCREEN_H)

    root = tk.Tk()
    all_windows = []

    def setup_window(win, x, y):
        win.title('温馨提示')
        win.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")
        win.resizable(False, False)
        win.attributes('-topmost', True)
        win.protocol("WM_DELETE_WINDOW", close_all)
        tip = random.choice(tips)
        bg = random.choice(bg_colors)
        tk.Label(win, text=tip, bg=bg, font=('微软雅黑', 13), width=22, height=2).pack()
        win.update_idletasks()
        win.deiconify()
        win.lift()

    def show_windows():
        activate_current_app()

        first_x, first_y = points_start[0]
        setup_window(root, first_x, first_y)
        try:
            root.focus_force()
        except tk.TclError:
            pass
        all_windows.append(root)

        for x, y in points_start[1:]:
            win = tk.Toplevel(root)
            setup_window(win, x, y)
            all_windows.append(win)
            root.update()
            time.sleep(0.015)

        root.after(900, move_to_heart)

    def animate_to_targets(targets, move_step, step_delay, pause_ms, next_action):
        max_steps = max(60, int(math.hypot(SCREEN_W, SCREEN_H) / move_step) + 12)
        for _ in range(max_steps):
            finished = True
            for i, win in enumerate(all_windows):
                cur_geo = win.geometry()
                cur_pos = cur_geo.split('+')[1:]
                x0, y0 = int(cur_pos[0]), int(cur_pos[1])
                xt, yt = targets[i]
                dx = xt - x0
                dy = yt - y0
                dist = math.hypot(dx, dy)
                if dist >= 2:
                    move = min(move_step, dist)
                    nx = x0 + int(move * dx / dist)
                    ny = y0 + int(move * dy / dist)
                    win.geometry(f"{WINDOW_W}x{WINDOW_H}+{nx}+{ny}")
                    finished = False
                else:
                    win.geometry(f"{WINDOW_W}x{WINDOW_H}+{xt}+{yt}")
            root.update()
            time.sleep(step_delay)
            if finished:
                for i, win in enumerate(all_windows):
                    xt, yt = targets[i]
                    win.geometry(f"{WINDOW_W}x{WINDOW_H}+{xt}+{yt}")
                root.update()
                break
        if next_action is not None:
            root.after(pause_ms, next_action)

    def move_to_heart():
        animate_to_targets(points_heart, HEART_STEP, HEART_FRAME_DELAY, HEART_PAUSE_MS, scatter_from_heart)

    def scatter_from_heart():
        animate_to_targets(points_scatter, SCATTER_STEP, SCATTER_FRAME_DELAY, 0, None)

    def close_all():
        for w in all_windows[1:]:
            if w.winfo_exists():
                w.destroy()
        if root.winfo_exists():
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_all)
    root.bind_all("<Escape>", lambda event: close_all())
    root.after(100, show_windows)
    root.mainloop()
