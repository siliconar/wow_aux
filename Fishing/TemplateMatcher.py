import cv2
import numpy as np
from PIL import Image
import pyautogui
import random
import os
from PIL import ImageGrab



class TemplateMatcher:
    def __init__(self):
        """
        初始化类，模板图片占位
        """
        self.template1 = None
        self.cnt =0;
        # self.template2 = None

    def load_templates(self, template1_path: str):
        """
        加载两个模板图片
        :param template1_path: 模板1图片的路径
        :param template2_path: 模板2图片的路径
        """
        self.template1 = cv2.imread(template1_path, cv2.IMREAD_COLOR)
        # self.template2 = cv2.imread(template2_path, cv2.IMREAD_COLOR)

        if self.template1 is None:
            raise ValueError("无法加载模板图片，请检查路径是否正确")

    def capture_screen_area(self, region: tuple, n_frames):
        """
        截取屏幕区域，连续截取5帧，返回帧的列表
        :param region: 截图区域 (x, y, width, height)
        :return: 连续帧的列表
        """
        x, y, width, height = region
        frames = []
        for _ in range(n_frames):  # 如果老匹配不成功，也可以改这个，截取的图片少一些
            # 截取屏幕区域并转换为 NumPy 数组

            bbox = (x, y, x+width, y+height)
            screenshot = ImageGrab.grab(bbox=bbox,all_screens= True)
            # screenshot = pyautogui.screenshot(region=(x, y, width, height))
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # 转换为 OpenCV 格式
            frames.append(frame)
        return frames

    def convolve2(self, frames: list, save_path: str, is_save:bool):
        """
        对每一帧图像与模板1进行卷积，寻找模板所在位置，
        并在一张截图上标记模板匹配点，保存图片。
        :param frames: 截取的连续帧的列表
        :param save_path: 保存标记结果的图片路径
        """
        if self.template1 is None:
            raise ValueError("模板1尚未加载，请调用 load_templates 方法加载模板")

        positions = []  # 存储每一帧的匹配位置

        for frame in frames:
            # 转换为灰度图像
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_template = cv2.cvtColor(self.template1, cv2.COLOR_BGR2GRAY)

            # 使用模板匹配
            res = cv2.matchTemplate(gray_frame, gray_template, cv2.TM_CCOEFF_NORMED)

            # 获取最大匹配点
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            # 假设匹配值大于阈值，记录位置
            if max_val > 0.8:  # 可调整阈值
                positions.append(max_loc)

        # 检查位置是否在所有帧中一致
        if len(positions) == len(frames) and all(pos == positions[0] for pos in positions):
            # 找到最终结果
            center = (positions[0][0] + self.template1.shape[1] // 2,
                      positions[0][1] + self.template1.shape[0] // 2)


            if is_save == True:  #如果的确要保存
                # 在其中一张图片上绘制标记
                marked_frame = frames[0].copy()
                cv2.circle(marked_frame, center, radius=10, color=(0, 255, 0), thickness=2)

                # 保存标记结果
                cv2.imwrite(save_path, marked_frame)
                print(f"标记结果已保存至: {save_path}")
            else:
                print("标记结果成功")
            return center

        else:
            print("未找到一致的匹配位置，可能存在误差或模板未在所有帧中出现")
            return None

    # def find_largest_changed_region(self, frames: list, save_path: str, is_save:bool) -> tuple:
    #     """
    #     找到两张图像中变化的区域，并返回变化区域中面积最大的连续区域的中心点。
    #     :param frames: 包含两张图像的列表，顺序为 [第一张图像, 第二张图像]
    #     :return: 面积最大的变化区域的中心点 (x, y)
    #     """
    #     if len(frames) != 2:
    #         raise ValueError("frames 列表必须包含两张图像")
    #
    #     # 转换为灰度图像
    #     gray_frame1 = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
    #     gray_frame2 = cv2.cvtColor(frames[1], cv2.COLOR_BGR2GRAY)
    #
    #     # 计算两张图像的绝对差异
    #     diff = cv2.absdiff(gray_frame1, gray_frame2)
    #
    #     # 二值化处理突出差异区域
    #     # _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    #     _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    #     # 寻找所有的轮廓
    #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    #     if not contours:
    #         raise ValueError("未检测到变化区域")
    #
    #     # 找到面积最大的轮廓
    #     max_contour = max(contours, key=cv2.contourArea)
    #
    #     # 计算最大区域的中心
    #     M = cv2.moments(max_contour)
    #     if M["m00"] == 0:
    #         raise ValueError("无法计算最大区域的中心")
    #     center_x = int(M["m10"] / M["m00"])
    #     center_y = int(M["m01"] / M["m00"])
    #     center = (center_x,center_y)
    #     if is_save == True:  # 如果的确要保存
    #         # 在其中一张图片上绘制标记
    #         marked_frame = frames[1].copy()
    #         cv2.circle(marked_frame, center, radius=10, color=(0, 255, 0), thickness=2)
    #
    #         # 保存标记结果
    #         cv2.imwrite(save_path, marked_frame)
    #         print(f"标记结果已保存至: {save_path}")
    #
    #
    #     return center_x, center_y
    def find_largest_changed_region(self, frames: list, save_path: str, is_save: bool) -> list:
        """
        找到两张图像中变化的区域，并返回变化区域中面积最大的 5 个连续区域的中心点。
        :param frames: 包含两张图像的列表，顺序为 [第一张图像, 第二张图像]
        :param save_path: 保存标记结果的图片路径
        :param is_save: 是否保存标记结果
        :return: 面积最大的 5 个变化区域的中心点列表 [(x1, y1), (x2, y2), ...]
        """
        if len(frames) != 2:
            raise ValueError("frames 列表必须包含两张图像")

        # 转换为灰度图像
        gray_frame1 = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.cvtColor(frames[1], cv2.COLOR_BGR2GRAY)

        # 计算两张图像的绝对差异
        diff = cv2.absdiff(gray_frame1, gray_frame2)

        # 二值化处理突出差异区域
        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

        # 寻找所有的轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            raise ValueError("未检测到变化区域")

        # 按轮廓面积从大到小排序
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # 提取前 5 个最大的轮廓
        top_contours = sorted_contours[:2]

        centers = []
        for contour in top_contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:  # 防止除以 0
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                centers.append((center_x, center_y))

        if is_save:  # 如果需要保存
            # 在其中一张图片上绘制标记
            marked_frame = frames[1].copy()
            for center in centers:
                cv2.circle(marked_frame, center, radius=10, color=(0, 255, 0), thickness=2)

            # 保存标记结果
            name, ext = os.path.splitext(save_path)
            save_path = name + str(self.cnt)+ext;
            self.cnt= self.cnt+1;
            cv2.imwrite(save_path, marked_frame)
            print(f"标记结果已保存至: {save_path}")

        return centers

    #检查是否中鱼
    def is_got_fish(self, img1_cut: np.ndarray, img2_cut: np.ndarray, is_save:bool) -> bool:

        if is_save == True:  # 如果的确要保存
            cv2.imwrite('bot.png', img2_cut)

        # 白点判定的阈值
        threshold = 150

        # 判断白点（接近 [255, 255, 255]）
        white_points_img1 = np.all(img1_cut >= threshold, axis=2)
        white_points_img2 = np.all(img2_cut >= threshold, axis=2)

        # 统计白点数量
        white_count_img1 = np.sum(white_points_img1)  # 像素点数
        white_count_img2 = np.sum(white_points_img2)
        # 计算白点变化
        white_diff = white_count_img2 - white_count_img1
        # 判定是否出现大量白点
        significant_increase = white_diff > 0.006 * img1_cut.shape[0] * img1_cut.shape[1]  # 假设变化超过1%为显著增加

        if significant_increase:
            return True
        return False

    def ransac_find_x0_y0(self, tuples, threshold=1.0, iterations=100):
        best_x0, best_y0 = None, None
        max_inliers = 0
        best_inliers = []

        # Flatten all points from the tuples for RANSAC sampling
        all_points = [point for t in tuples for point in t]

        for _ in range(iterations):
            # Randomly select a point as the hypothesis
            x0, y0 = random.choice(all_points)

            # Calculate inliers: points within the threshold distance
            inliers = []
            for t in tuples:
                for point in t:
                    distance = np.sqrt((point[0] - x0) ** 2 + (point[1] - y0) ** 2)
                    if distance < threshold:
                        inliers.append(point)

            # Update best hypothesis if current inliers are the most
            if len(inliers) > max_inliers:
                max_inliers = len(inliers)
                best_x0, best_y0 = x0, y0
                best_inliers = inliers

        # Find the closest point to the best_x0, best_y0 in each tuple
        closest_points = []
        for t in tuples:
            closest_point = min(t, key=lambda p: np.sqrt((p[0] - best_x0) ** 2 + (p[1] - best_y0) ** 2))
            closest_points.append(closest_point)

        return best_x0, best_y0

# # 使用示例
# if __name__ == "__main__":
#     # 初始化匹配类
#     matcher = TemplateMatcher()
#
#     # 加载两个模板图片
#     matcher.load_templates("template_3.png")
#
#     # 定义截屏区域并保存至指定目录
#     # region_to_capture = (100, 100, 300, 300)  # 定义屏幕区域
#     # save_directory = "./frames"  # 保存路径
#     # captured_frames = matcher.capture_screen_area(region_to_capture, save_directory)
#
#     captured_frames = []
#     for i in range(5):
#         frame = cv2.imread("5.png", cv2.IMREAD_COLOR)
#         captured_frames.append(frame)
#     # 对每一帧与模板1进行卷积并显示
#     matcher.convolve2(captured_frames,'save111.png', True)