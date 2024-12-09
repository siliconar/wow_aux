import ctypes
from win32gui import FindWindow
from win32con import WM_LBUTTONDOWN, WM_LBUTTONUP

# 获取窗口句柄
hwnd = FindWindow(None, "微信")

# 模拟鼠标左键点击
x, y = 155, 90  # 窗口内部坐标
l_param = (y << 16) | x  # 将坐标打包成 lParam 格式

ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 0, l_param)  # 按下
ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, l_param)    # 松开