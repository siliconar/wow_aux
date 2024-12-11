
# 2302 1014

from MouseOperation import *

# 初始化 MouseOperation
mouse1 = MouseOperation()
hwnd = mouse1.find_window("魔兽世界")
if hwnd == None:
    print("魔兽世界寻找失败")
    exit()



mouse1.send_mouse_click_right(2302-1920, 985)
# mouse1.send_mouse_click_left(40, 262)
