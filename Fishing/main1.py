import time

from WindowKeyPresser2 import *
from TemplateMatcher import *
from MouseOperation import *
import random

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
# matcher1.load_templates("template_4.png") #加载模板
#定义截屏区域并保存至指定目录
startx, starty = 521, 25
endx,endy = 1517, 791
region_to_capture1 = (startx,starty,endx-startx, endy-starty )  # 定义屏幕区域



##--- 正式开始

time.sleep(3)


for kkk in range(10):
    print("第"+str(kkk)+"次钓鱼")

    # 随机暂停1到3秒
    pause_time = random.uniform(1, 3)  # 生成1到3之间的随机浮点数
    time.sleep(pause_time)  # 暂停指定的秒数

    # 建立前后两帧存储器
    captured_frames = [];

    # 先截取抛竿前的一帧
    frames = matcher1.capture_screen_area(region_to_capture1, 1)
    captured_frames.append(frames[0])

    #抛出一杆
    presser1.send_key("1")  #抛出一杆
    time.sleep(2)
    # 截取抛竿后的一帧
    frames = matcher1.capture_screen_area(region_to_capture1, 1)
    captured_frames.append(frames[0])

    # 通过模板比较
    # center1 = matcher1.convolve2(captured_frames,'save111.png', True)   # 对每一帧与模板1进行卷积并显示
    # if center1 == None:
    #     print("未找到中心")
    #     exit()
    # 通过前后帧比较
    center1 = matcher1.find_largest_changed_region(captured_frames, 'save111.png', False)
    time.sleep(1)


    ##-- 判断是否中鱼

    #鱼漂截图范围
    fishbot_x = center1[0]
    fishbot_y = center1[1]
    fishbot_w = 61
    fishbot_h = 69

    # 设立鱼漂基准切片
    tmp_img = captured_frames[1]
    img1_cut = tmp_img[fishbot_y:fishbot_y+fishbot_h, fishbot_x:fishbot_x+fishbot_w, :]  # 这里注意，因为是numpy，所以xy一定交换位置

    # 设置循环开始时间
    start_time = time.time()

    while True:
        # 获取当前时间
        current_time = time.time()

        # 判断是否超过30秒
        if current_time - start_time >= 25:
            print("超过30秒，退出循环")
            break

        # 执行循环内容
        frames = matcher1.capture_screen_area(region_to_capture1, 1)

        # 设立当前鱼漂切片
        tmp_img = frames[0]
        img2_cut = tmp_img[fishbot_y:fishbot_y+fishbot_h, fishbot_x:fishbot_x+fishbot_w, :]  # 这里注意，因为是numpy，所以xy一定交换位置


        bgotfish = matcher1.is_got_fish(img1_cut,img2_cut,False)
        #如果中鱼了
        if bgotfish == True:
            # 换算真实地址
            real_x = startx + center1[0];
            real_y = starty + center1[1];
            mouse1.send_mouse_click_right(real_x, real_y)
            break;










