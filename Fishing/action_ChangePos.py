
import  time

class action_ChangePos:
    def __init__(self,  keyboard_driver ):
        # 注册各个驱动组件
        self.presser1 = keyboard_driver

        # 自己的变量
        self.lastdir = 1;  #1是左边，#2是右边
        return


    def changePos(self):

        # 换方向
        if self.lastdir==1:
            self.lastdir=2;
        else:
            self.lastdir=1;

        str_btn = "";
        if self.lastdir == 1:
            str_btn = "s"
        else:
            str_btn = "d"

        #执行操作
        self.presser1.keydown(str_btn);
        time.sleep(0.2)
        self.presser1.keyup(str_btn);