from action_FishOnce import  *



# 获取窗口句柄函数
def get_window_handles_by_title(title):
    """获取所有匹配标题的窗口句柄"""
    def enum_windows_callback(hwnd, handles):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            handles.append(hwnd)
    handles = []
    win32gui.EnumWindows(enum_windows_callback, handles)
    return handles


# 初始化 MouseOperation
mouse1 = MouseOperation()
hwnd = mouse1.find_window("魔兽世界")
if hwnd == None:
    print("魔兽世界寻找失败")
    exit()

# 初始化WindowKeyPresser2
window_title = "魔兽世界"  # 替换为窗口标题
windows = get_window_handles_by_title(window_title)
window_1 = windows[0]  # 第一个窗口句柄
presser1 = WindowKeyPresser("魔兽世界",window_1)  # 替换为实际窗口标题


# 初始化TemplateMatcher， 图像识别器
matcher1 = TemplateMatcher()


# 初始化行动层
actioner_Fish1 = action_FishOnce(mouse1, presser1,matcher1)
actioner_Fish1.init();




actioner_Fish1.FishOnce();





