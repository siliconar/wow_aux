import ctypes


class MouseOperation:
    def __init__(self):
        # 定义 Windows API 函数
        self.SendMessage = ctypes.windll.user32.SendMessageW
        self.FindWindow = ctypes.windll.user32.FindWindowW

        # 定义鼠标消息常量
        self.WM_MOUSEMOVE = 0x0200
        self.WM_LBUTTONDOWN = 0x0201
        self.WM_LBUTTONUP = 0x0202
        self.WM_RBUTTONDOWN = 0x0204
        self.WM_RBUTTONUP = 0x0205

    def find_window(self, window_name):
        """
        查找窗口句柄
        :param window_name: 窗口标题
        :return: 窗口句柄（整数），未找到返回 None
        """
        hwnd = self.FindWindow(None, window_name)
        if hwnd:
            self.hwnd = hwnd
            return hwnd
        else:
            print(f"未找到窗口: {window_name}")
            return None

    def send_mouse_click_left(self, x, y):
        """
        向指定窗口发送鼠标点击事件
        :param hwnd: 窗口句柄
        :param x: 点击的 X 坐标
        :param y: 点击的 Y 坐标
        """
        lParam = y << 16 | x
        self.SendMessage(self.hwnd, self.WM_MOUSEMOVE, 0, lParam)  # 鼠标移动
        self.SendMessage(self.hwnd, self.WM_LBUTTONDOWN, 1, lParam)  # 鼠标按下
        self.SendMessage(self.hwnd, self.WM_LBUTTONUP, 0, lParam)  # 鼠标松开

    def send_mouse_click_right(self, x, y):
        """
        向指定窗口发送鼠标点击事件
        :param hwnd: 窗口句柄
        :param x: 点击的 X 坐标
        :param y: 点击的 Y 坐标
        """
        lParam = y << 16 | x
        self.SendMessage(self.hwnd, self.WM_MOUSEMOVE, 0, lParam)  # 鼠标移动
        self.SendMessage(self.hwnd, self.WM_RBUTTONDOWN, 1, lParam)  # 鼠标按下
        self.SendMessage(self.hwnd, self.WM_RBUTTONUP, 0, lParam)  # 鼠标松开