



import win32gui
import win32con
import win32api
import time


class WindowKeyPresser:
    def __init__(self, window_title, hwnd):
        """初始化类，指定窗口标题"""
        self.window_title = window_title
        self.hwnd = hwnd
        # 获取虚拟键码
        self.vk_code = {
            "space": 0x20,  # 空格键
            "enter": 0x0D,  # 回车键
            "left_alt": 0x11,  # 左 Alt 键
            "left_ctrl": 0x12,  # 左 Ctrl 键
            "left_shift": 0x10,  # 左 Shift 键
            "z": 0x5A,      # z键
            "w": 0x57,  # W 键
            "a": 0x41,  # A 键
            "s": 0x53,  # S 键
            "d": 0x44,  # D 键
            "e": 0x45,  # E 键
            "t": 0x54,  # T 键
            "f": 0x46,  # F 键
            "q": 0x51,  # Q 键
            "g": 0x47,  # G 键
            "h": 0x48,  # H 键
            "i": 0x49,  # I 键
            "j": 0x4A,  # J 键
            "k": 0x4B,  # K 键
            "u": 0x55,  # U 键

            "f1": 0x70,  # U 键

            "1": 0x31,  # 数字键 1
            "2": 0x32,  # 数字键 2
            "3": 0x33,  # 数字键 3
            "4": 0x34,  # 数字键 4
            "5": 0x35,  # 数字键 5
            "6": 0x36,      # 数字6
            "7": 0x37,      # 数字7
            "8": 0x38,      # 数字8
            "9": 0x39,      # 数字9
            "0": 0x30       # 数字0
        }


    # def get_window_handles_by_title(self):
    #     """获取所有匹配标题的窗口句柄"""
    #     def enum_windows_callback(hwnd, handles):
    #         if win32gui.IsWindowVisible(hwnd) and self.window_title in win32gui.GetWindowText(hwnd):
    #             handles.append(hwnd)
    #     handles = []
    #     win32gui.EnumWindows(enum_windows_callback, handles)
    #     return handles
    #
    # def get_window_handle(self):
    #     """获取单个窗口句柄（假设取第一个匹配的窗口）"""
    #     handles = self.get_window_handles_by_title()
    #     if not handles:
    #         print(f"未找到匹配的窗口: {self.window_title}")
    #         return None
    #     print(f"找到的窗口句柄: {handles}")
    #     return handles[0]

    def send_key(self, key):
        """向指定窗口发送按键事件（后台发送，不切换窗口）"""
        if not self.hwnd:
            print(f"未找到窗口句柄，无法发送按键: {key}")
            return

        vk_code1 = self.vk_code.get(key)

        if not vk_code1:
            print(f"不支持的按键: {key}")
            return

        # 模拟按键按下和释放事件
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code1, 0)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code1, 0)
        print(f"已向窗口发送按键: {key}")



    def keydown(self, key):
        vk_code1 = self.vk_code.get(key)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, vk_code1, 0)

    def keyup(self, key):
        vk_code1 = self.vk_code.get(key)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, vk_code1, 0)

    def start_pressing_key(self, key, interval=60):
        """开始定时按键"""
        if not self.hwnd:
            print("无法开始定时按键，未找到窗口句柄。")
            return

        try:
            while True:
                self.send_key(key)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("按键操作已停止。")

