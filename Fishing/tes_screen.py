
from PIL import ImageGrab


from PIL import ImageGrab

# 指定区域
left = 1920   # 截图区域左上角的X坐标
top = 0    # 截图区域左上角的Y坐标
right = 1920*2  # 截图区域右下角的X坐标
bottom = 1080 # 截图区域右下角的Y坐标

# 截图指定区域
bbox = (left, top, right, bottom)
screenshot = ImageGrab.grab(bbox=bbox,all_screens= True)

# 保存截图
screenshot.save("screenshot.png")
print("截图已保存为 screenshot.png")

