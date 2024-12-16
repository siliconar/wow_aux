import time

from WindowKeyPresser2 import *
from TemplateMatcher import *
from MouseOperation import *
import random


#### 钓鱼基础——基础行动层10
# 抛
# 识别鱼漂
# 随机失败
# 鱼漂跳动，点击


class action_FishOnce:
    def __init__(self, mouse_driver, keyboard_driver, matcher_driver ):
        # 注册各个驱动组件
        self.mouse1 = mouse_driver;
        self.presser1 = keyboard_driver
        self.matcher1 = matcher_driver
        return

    def init(self):
        # 定义截屏区域并保存至指定目录
        startx, starty = 521, 25
        endx, endy = 1517, 791
        # startx, starty = 1920+521, 25
        # endx, endy = 1920+1517, 791
        self.region_to_capture1 = (startx, starty, endx - startx, endy - starty)  # 定义屏幕区域
        self.startx = startx
        self.starty = starty

    def FishOnce(self):
        # 开始掉一次鱼
        # 建立前后两帧存储器
        ransac_center_tuples = []  # 用于存储变化点的tuple
        captured_frames = [];

        # 先截取抛竿前的一帧
        frames = self.matcher1.capture_screen_area(self.region_to_capture1, 1)
        captured_frames.append(frames[0])

        # 抛出一杆
        self.presser1.send_key("1")  # 抛出一杆
        time.sleep(2)


        for kb in range(5):
            # 截取抛竿后的一帧
            frames = self.matcher1.capture_screen_area(self.region_to_capture1, 1)
            if len(captured_frames)==1:  #如果只有1张图，也就是第一次进循环
                captured_frames.append(frames[0])
            else:
                captured_frames[1] = frames[0]
            # 通过前后帧比较,确定鱼漂位置
            center_5 = self.matcher1.find_largest_changed_region(captured_frames, 'save111.png', True)
            ransac_center_tuples.append(center_5) #记录center
            time.sleep(0.2)

        # 进行ransac选出最终点
        best_x0, best_y0 = self.matcher1.ransac_find_x0_y0(ransac_center_tuples, threshold=3, iterations=1000)
        center1 = [best_x0, best_y0]

        ##-- 判断是否中鱼

        # 鱼漂截图范围
        fishbot_x = center1[0]
        fishbot_y = center1[1]
        fishbot_w = 61
        fishbot_h = 69

        # 设立鱼漂基准切片
        tmp_img = captured_frames[1]
        img1_cut = tmp_img[fishbot_y:fishbot_y + fishbot_h, fishbot_x:fishbot_x + fishbot_w, :]  # 这里注意，因为是numpy，所以xy一定交换位置

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
            frames = self.matcher1.capture_screen_area(self.region_to_capture1, 1)

            # 设立当前鱼漂切片
            tmp_img = frames[0]
            img2_cut = tmp_img[fishbot_y:fishbot_y + fishbot_h, fishbot_x:fishbot_x + fishbot_w, :]  # 这里注意，因为是numpy，所以xy一定交换位置

            bgotfish = self.matcher1.is_got_fish(img1_cut, img2_cut, True)
            # 如果中鱼了
            if bgotfish == True:
                # 换算真实地址
                # real_x = self.startx + center1[0];
                # real_y = self.starty + center1[1];
                real_x = self.startx + center1[0]-1920 ; # 坐标是相对于窗口的，不加1920
                real_y = self.starty + center1[1]; # 坐标是相对于窗口的，不加1920

                print(str(real_x) + "-" + str(real_y))

                self.mouse1.send_mouse_click_right(real_x, real_y)
                break;
