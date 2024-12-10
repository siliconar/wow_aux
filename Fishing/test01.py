import ctypes

# 定义 Windows API 函数和常量
SendMessage = ctypes.windll.user32.SendMessageW
FindWindow = ctypes.windll.user32.FindWindowW
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202

def send_mouse_click(hwnd, x, y):
    lParam = y << 16 | x
    SendMessage(hwnd, WM_MOUSEMOVE, 0, lParam)  # 鼠标移动
    SendMessage(hwnd, WM_LBUTTONDOWN, 1, lParam)  # 鼠标按下
    SendMessage(hwnd, WM_LBUTTONUP, 0, lParam)  # 鼠标松开

# 查找窗口
hwnd = FindWindow(None, "魔兽世界")
if hwnd:
    send_mouse_click(hwnd, 373,983)  #注意这个坐标没有标题栏
else:
    print("未找到窗口")