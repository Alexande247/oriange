import sys
import random
from socket import *
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow
from Form import Ui_MainWindow

ip = "192.168.0.5"   # 雅马哈机器人ip地址，记得连接机器人需要改电脑IP
port = 23   # 通信端口

# 创建标识  用来做发送后二次校验  目前没做二次校验。
Step_state = {"connect_state": False, "start1_state": False, "run1_state": False,
              "stop1_state": False, "reset1_state": False, "start2_state": False,
              "run2_state": False, "stop2_state": False}

# 步骤转命令
Step_cmd = {"run1": "@ RUN <LJFJLSX>",
            "run_reboot": "@ SO11()=&B00000001",
            "stop1": "@ STOP <LJFJLSX>",
            "reset1": "@ RESET <LJFJLSX>",
            "run2": "@ RUN <TASKTWO>",
            "stop2": "@ STOP <TASKTWO>",
            "reset2": "@ RESET <TASKTWO>",
            "set_v": "@ SOW(8)=&H00",
            "clean_err": "@ SO10()=&B00000001",
            "read_belt": "@ READ SIW(0)",
            "read_gripper": "@ READ SO2()",
            "read_err": "@ READ SO7()",
            "run_cylinder": "@ SO3()=&B00000001",
            "reset_cylinder": "@ SO5()=&B00000001",
            "S01":"@ SO5()=&B00000001",
            }


class MyPyQT_Form(Ui_MainWindow):

    def __init__(self, Ui_MainWindow):
        # 继承生成的Ui_Form类

        self.setupUi(Ui_MainWindow)
        # self.load_program()   载入程序
        self.connect_slot()
        self.error_protected(False)
        # 添加按钮事件

    # 防误操
    def error_protected(self, key):   # 设置误触
        self.run_1.setEnabled(key)
        self.set_v.setEnabled(key)
        self.run_reboot.setEnabled(key)
        self.stop_1.setEnabled(key)
        self.reset_1.setEnabled(key)
        self.run_2.setEnabled(key)
        self.stop_2.setEnabled(key)
        self.reset_2.setEnabled(key)
        self.read_err.setEnabled(key)
        self.clean_err.setEnabled(key)
        self.run_cylinder.setEnabled(key)
        self.reset_cylinder.setEnabled(key)
        self.read_belt.setEnabled(key)
        self.read_gripper.setEnabled(key)

    # 连接机器人
    def tcp_connect(self):
        self.connect_reboot.setEnabled(False)
        self.error_protected(True)
        self.tcp_c = socket(AF_INET, SOCK_STREAM)
        self.tcp_c.bind(('192.168.0.3', random.randint(3000, 65535)))  # 绑定用户主机ip
        print("开始与机器人建立连接...")
        self.read.setText("开始与机器人建立连接...")
        for i in range(10):
            try:
                self.tcp_c.connect((ip, port))  # 建立连接
                Step_state["connect_state"] = True
                sleep(1)  # 等待连接响应
            except:
                self.read.setText("连接失败，尝试第" + str(i + 1) + "次重连...")
                Step_state["connect_state"] = False
                if i == 9:
                    self.read.setText("连接失败，请检查网络链路。")
                    exit(199)
            else:
                self.read.setText("连接机器人成功！")
                sleep(0.01)
                # connect_feedback = self.tcp_c.recv(1024)
                # print(connect_feedback.decode('gbk'))
                # self.load_program()
                break
        sleep(1)
        self.load_program()

    # 载入机器人点位目前未做使用
    def load_point(self):
        # P1 = input("输入起点：")
        # P2 = input("输入终点：")
        # x y z r a b (左手：2,右手：1) xyz坐标，r旋转角度：角度制(-180~360)  z默认7  00200默认
        P1 = "139.765 184.537 6.945 -125.373 0 0 2 0 0\r\n"  # 起点
        P2 = "248.014 212.245 6.945 -125.373 0 0 2 0 0\r\n"  # 终点

        data1 = "@ P1=" + P1
        data2 = "@ P2=" + P2
        self.tcp_c.send(bytes("@ SOW(3)=&H0000\r\n", encoding="utf8"))
        # 0000标明循环一次，是一个十六进制数，表示垃圾个数
        data1 = bytes(data1, encoding="utf8")
        self.tcp_c.send(data1)
        # data = self.tcp_c.recv(1024)
        # print(data.decode('gbk'))

        data2 = bytes(data2, encoding="utf8")
        self.tcp_c.send(data2)
        sleep(0.01)
        data = self.tcp_c.recv(1024)
        print(data.decode('gbk'))

    # 发送转状态码做二次校验，同时接收发送反馈
    def recv_to_state(self, step):
        sleep(0.01)  # 延时等待机器人反馈
        recv = self.tcp_c.recv(1024).decode('gbk')  # 接收机器人反馈
        if (recv == "OK\r\n"):
            Step_state[step] = True
            print("***命令执行成功***\n")
            self.read.setText("***命令执行成功***\n")
        elif (recv == "NG=6.215\r\n"):
            self.read.setText("***程序已经执行!***\n")
            print("***程序已经执行!***\n")
            Step_state[step] = True
            # print(Step_state[step])
        elif (recv == "NG=3.237\r\n"):
            self.read.setText("***程序已经存在！***\n")
            print("***程序已经存在！***\n")
            Step_state[step] = True
            # print(Step_state[step])
        else:
            self.read.setText("***请参考用户手册***\n"+recv)
            print("***请参考用户手册***\n", recv)

    # 读取查询指令
    def read_state(self, cmd):
        # 发送查询指令
        self.tcp_c.send(bytes(cmd + "\r\n", encoding="utf8"))
        sleep(0.01)
        recv = self.tcp_c.recv(1024).decode('gbk')  # 接收机器人反馈
        self.read.setText(recv)

    # 开机载入程序
    def load_program(self):
        self.tcp_c.send(bytes("@ RUN <LJFJLSX>\r\n", encoding="utf8"))
        self.recv_to_state("start1_state")

        self.tcp_c.send(bytes("@ START <TASKTWO>\r\n", encoding="utf8"))
        self.recv_to_state("start2_state")

    # 发送指令转换
    def sendto_command(self, cmd):
        # 转字节数据
        self.tcp_c.send(bytes(cmd + "\r\n", encoding="utf8"))
        self.recv_to_state("start2_state")

    # 按钮交互逻辑
    def connect_slot(self):
        # 按钮触发函数
        self.connect_reboot.clicked.connect(self.tcp_connect)
        # 设置10进制转16进制且去掉前面的0x同时补0(15以下的十进制数去掉0x后只有一位，需补0)然后改为大写
        self.set_v.clicked.connect(lambda: self.sendto_command(Step_cmd["set_v"]+('%02x' % int(self.input_v.toPlainText())).upper()))

        self.run_1.clicked.connect(lambda: self.sendto_command(Step_cmd["run1"]))
        self.run_reboot.clicked.connect(lambda: self.sendto_command(Step_cmd["run_reboot"]))
        self.stop_1.clicked.connect(lambda: self.sendto_command(Step_cmd["stop1"]))
        self.reset_1.clicked.connect(lambda: self.sendto_command(Step_cmd["reset1"]))

        self.run_2.clicked.connect(lambda: self.sendto_command(Step_cmd["run2"]))
        self.stop_2.clicked.connect(lambda: self.sendto_command(Step_cmd["stop2"]))
        self.reset_2.clicked.connect(lambda: self.sendto_command(Step_cmd["reset2"]))
        self.read_err.clicked.connect(lambda: self.read_state(Step_cmd["read_err"]))

        self.clean_err.clicked.connect(lambda: self.sendto_command(Step_cmd["clean_err"]))
        self.run_cylinder.clicked.connect(lambda: self.sendto_command(Step_cmd["run_cylinder"]))
        self.reset_cylinder.clicked.connect(lambda: self.sendto_command(Step_cmd["reset_cylinder"]))

        self.read_belt.clicked.connect(lambda: self.read_state(Step_cmd["read_belt"]))
        # self.read_gripper.clicked.connect(lambda: self.read_state(Step_cmd["read_gripper"]))

        # self.read_gripper.clicked.connect(lambda: self.read_state("@ SO5()=&B00000010\n"))
        self.read_gripper.clicked.connect(self.RunAuto)  # 自动化控制函数


    #自动化控制逻辑
    def RunAuto(self):
        # 第一排，气缸组1
        # 第一步指令
        self.read_state("@ SO3()=&B00000001")
        # 发送延时
        sleep(5)
        # 第二条指令
        self.read_state("@ SO5()=&B00000001")
        #2023-4-27 新添加
        # 第二排，气缸组3、4
        # 第一步指令
        self.read_state("@ SO3()=&B00000100")
        self.read_state("@ SO3()=&B00001000")
        # 发送延时
        sleep(5)
        # 第二条指令
        self.read_state("@ SO5()=&B00000100")
        self.read_state("@ SO5()=&B00001000")
        # 第三排，气缸组5
        # 第一步指令
        self.read_state("@ SO3()=&B00010000")
        # 发送延时
        sleep(5)
        # 第二条指令
        self.read_state("@ SO5()=&B00010000")
        # 第四排，气缸组8
        # 第一步指令
        self.read_state("@ SO3()=&B10000000")
        # 发送延时
        sleep(5)
        # 第二条指令
        self.read_state("@ SO5()=&B10000000")
        # 第五排，气缸组9
        # 第一步指令
        self.read_state("@ SO4()=&B00000001")
        # 发送延时
        sleep(5)
        # 第二条指令
        self.read_state("@ SO6()=&B00000001")










if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = MyPyQT_Form(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())




