import cv2
import numpy as np

# 读取图像
img1 = cv2.imread('1.png')
img2 = cv2.imread('2.png')

# 裁剪感兴趣区域
img1_cut = img1[217:277, 961:1029, :]
img2_cut = img2[217:277, 961:1029, :]

# 显示裁剪的第二幅图像
cv2.imshow('Image Cut', img2_cut)
cv2.waitKey(0)
cv2.destroyAllWindows()

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
significant_increase = white_diff > 0.01 * img1_cut.shape[0] * img1_cut.shape[1]  # 假设变化超过1%为显著增加
print(img1_cut.shape[0])
print(img1_cut.shape[1])

if significant_increase:
    print(f'图像中检测到大量白点的显著增加，增加了 {white_diff} 个白点。')
else:
    print(f'图像中的白点变化不显著，变化量为 {white_diff} 个白点。')
