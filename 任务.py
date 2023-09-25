# QTextEdit控件

# QTextLine只能输入一行文本，输入多行文本用QTextEdit  常用功能：获得文本和设置文本，除了支持普通的文本，还支持富文本(改变颜色，设置尺寸)

import sys

from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QApplication, QPushButton, QHBoxLayout, QWidget, QToolTip, QVBoxLayout, QLabel, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import *
import os
import time
import office
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# 导入调制板，调制QLabel背景色
# 导入显示图片包QPixmap
from PyQt5.QtGui import QPixmap,QPalette
# 导入一些Qt的常量
from PyQt5.QtCore import Qt

# 进入服务器网址
def get_url(url,driver):
    #最大化窗口界面
    driver.maximize_window()
    #进入网址
    driver.get(url)

#进入后等待一段时间
def wait(driver, time):
    driver.implicitly_wait(time)

#找到服务器下shadow_root位置并返回
def get_shadow(driver, js):
    return driver.execute_script(js)

#找到网址内输入文本框的位置并返回
def get_textbox(shadow, locator):
    return shadow.find_element(By.CSS_SELECTOR, locator)

#用户将想要输入的内容填入文本框中
def input_words(txtbox, content):
    txtbox.send_keys(content)

#找到网址内生成框的位置
def get_button(shadow, locator):
    return shadow.find_element(By.CSS_SELECTOR, locator)

#进行文字生成图片的操作
def generate(button):
    button.send_keys(Keys.ENTER)

#找到进入下一个页面的按钮所在位置
def get_n_button(driver, js):
    return driver.execute_script(js)

#进入下一个页面
def get_nxt(element):
    element.click()

#清空文本框中的文字
def clear(driver, js):
    driver.execute_script(js)

#找到网址内调整重绘幅度的位置
def get_s_box(shadow, s_locator):
    return shadow.find_element(By.CSS_SELECTOR, s_locator)

#对重绘幅度进行调整
def change_step(s_box, step):
    s_box.send_keys(step)

#生成草图
def first_generate(element):
    element.click()

#遍历生成的图片所在文件夹，并将其中的图片一一进行显示
def keep_file(files,path):
    n = 0
    for file in files:
        new_path = path + '\\0' + str(n) + '.png'
        img = Image.open(new_path)
        img.show()
        n += 1
        break

def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list

# 编写一个类，从QWidget里面继承
class QTextEditDemo(QWidget):
    def __init__(self):
        super(QTextEditDemo,self).__init__()
        self.initUI()

        #用户输入的正向关键词
        self.in1_content = ''

        # 用户输入的反向关键词
        self.in2_content = ''

        # 读取最终用户需要查看的图片位置
        self.fla = 0

        # 用于生成不同结果的判断变量
        self.f = 0

        #记录图片生成位置的变量
        self.n = 0

        #进入浏览器
        self.driver = ''

        #找到浏览器内shadow_root位置
        self.shadow = ''

        #四张图片的名字的存储
        self.name1 = ''
        self.name2 = ''
        self.name3 = ''
        self.name4 = ''
        self.name5 = ''


    # 编写初始化方法 规范代码，初始化写在一个方法里
    def initUI(self):
        # 设置窗口的标题
        self.setWindowTitle('画师')

        # 设置窗口的尺寸
        self.resize(600, 600)

        # 创建全局控件  为什么要创建去全局控件，在槽方法里需要调用
        # 文本框1用于存储正向提示词
        self.textEdit1 = QTextEdit()

        # 文本框2用于存储反向提示词
        self.textEdit2 = QTextEdit()

        # 文本框3用于存储流程显示
        self.textEdit3 = QTextEdit()


        # 标签框提示
        # 标签框1提示存储正向提示词
        label1 = QLabel(self)

        # 标签框2提示存储反向提示词
        label2 = QLabel(self)

        # 标签框3提示存储流程显示
        label3 = QLabel(self)

        # 标签框4用于提示操作
        self.label4 = QLabel(self)

        # 给label1设置文本,支持html的标签
        label1.setText("<font color=purpel>请输入正向提示词</font>")

        # 给label2设置文本,支持html的标签
        label2.setText("<font color=purpel>请输入反向提示词</font>")

        # 给label3设置文本,支持html的标签
        label3.setText("<font color=purpel>请输入1-4查看过程</font>")

        # 给label4设置文本,支持html的标签
        self.label4.setText("<font color=purpel>请在输入正向提示词后点击读入</font>")
        self.label4.repaint()

        #暂时不考虑颜色
        # # 用调试板自动填充背景
        # label4.setAutoFillBackground(True)
        # # 创建调试板
        # palette = QPalette()
        # # 给调试板设置背景色
        # palette.setColor(QPalette.Window, Qt.blue)
        # # 对label4使用调试板
        # label4.setPalette(palette)
        # 让label4居中对齐
        # label4.setAlignment(Qt.AlignCenter)


        # 创建全局按钮
        # 按钮一：获取文本
        # buttonToText1 = QPushButton('读入正向提示词')
        self.buttonToText1 = QPushButton('读入正向提示词')

        # 按钮二：获取文本
        # buttonToText2 = QPushButton('读入反向提示词')
        self.buttonToText2 = QPushButton('读入反向提示词')

        # 按钮三：生成最终图
        # buttonToText3 = QPushButton('生成图片')
        self.buttonToText3 = QPushButton('生成图片')

        # 按钮四：生成草图
        # buttonToText4 = QPushButton('生成过程中图片')
        self.buttonToText4 = QPushButton('生成过程中图片')

        # 按钮五：满意
        # buttonToText5 = QPushButton('满意')
        self.buttonToText5 = QPushButton('满意')

        # 按钮六：不满意
        # buttonToText6 = QPushButton('不满意')
        self.buttonToText6 = QPushButton('不满意')



        #创建布局
        #创建整体垂直布局
        wlayout = QVBoxLayout()

        # # 创建垂直布局
        # vlayout = QVBoxLayout()
        # vwg = QWidget()

        # 创建水平布局
        #水平布局1水平摆放文本框1和标签框1
        hlayout1 = QHBoxLayout()
        hwg1 = QWidget()
        hlayout1.addWidget(label1)
        hlayout1.addWidget(self.textEdit1)

        # 水平布局2水平摆放文本框2和标签框2
        hlayout2 = QHBoxLayout()
        hwg2 = QWidget()
        hlayout2.addWidget(label2)
        hlayout2.addWidget(self.textEdit2)

        # 水平布局3水平摆放文本框3和标签框3
        hlayout3 = QHBoxLayout()
        hwg3 = QWidget()
        hlayout3.addWidget(label3)
        hlayout3.addWidget(self.textEdit3)

        # 水平布局4水平摆放文本框4和标签框4
        hlayout4 = QHBoxLayout()
        hwg4 = QWidget()
        hlayout4.addWidget(self.buttonToText5)
        hlayout4.addWidget(self.buttonToText6)


        # 设置布局
        # 设置水平布局
        hwg1.setLayout(hlayout1)
        hwg2.setLayout(hlayout2)
        hwg3.setLayout(hlayout3)
        hwg4.setLayout(hlayout4)

        # 设置整体布局
        wlayout.addWidget(self.label4)
        self.label4.setAlignment(Qt.AlignCenter)
        wlayout.addWidget(hwg1)
        wlayout.addWidget(hwg2)
        wlayout.addWidget(hwg3)
        wlayout.addWidget(self.buttonToText1)
        wlayout.addWidget(self.buttonToText2)
        wlayout.addWidget(self.buttonToText3)
        wlayout.addWidget(self.buttonToText4)
        wlayout.addWidget(hwg4)

        # 创建垂直布局
        self.setLayout(wlayout)

        # # 创建垂直布局
        # vlayout = QVBoxLayout()
        #
        #
        # # 把控件添加到垂直布局里面
        # vlayout.addWidget(self.textEdit1)
        # vlayout.addWidget(self.textEdit2)
        # vlayout.addWidget(self.textEdit3)
        # # layout.addWidget(buttonText)
        # # layout.addWidget(buttonHTML)
        # vlayout.addWidget(self.buttonText)
        # vlayout.addWidget(self.buttonHTML)
        # vlayout.addWidget(self.buttonToText)
        # vlayout.addWidget(self.buttonToHTML)
        #
        # # 应用于垂直布局
        # vwg.setLayout(vlayout)
        # # self.setLayout(vlayout)
        #
        # # 创建一水平布局
        # hlayout = QHBoxLayout()
        # # 分别把这四个控件放到这个布局里面           布局函数 addWidget
        # hlayout.addWidget(self.textEdit1)
        # hlayout.addWidget(self.textEdit2)
        # # hbox.addWidget(label3)
        # # hbox.addWidget(label4)
        #
        # # 设置布局
        # # hwg.setLayout(hlayout)
        #
        # wlayout.addWidget(hwg)
        # wlayout.addWidget(vwg)
        #
        # self.setLayout(wlayout)


        # 把槽绑定到单击按钮信号上
        #     buttonText.clicked.connect(self.onClick_ButtonText)
        #     buttonHTML.clicked.connect(self.onClick_ButtonHTML)
        # 读取正向提示词
        self.buttonToText1.clicked.connect(self.onClick_buttonToText1)

        # 读取反向提示词
        self.buttonToText2.clicked.connect(self.onClick_buttonToText2)

        # 生成最终图
        self.buttonToText3.clicked.connect(self.onClick_ButtonToText3)

        # 生成流程所需显示图片
        self.buttonToText4.clicked.connect(self.onClick_buttonToText4)

        # 确认对当前图片满意
        self.buttonToText5.clicked.connect(self.onClick_buttonToText5)

        # 确认对当前图片不满意
        self.buttonToText6.clicked.connect(self.onClick_buttonToText6)


    # 定义槽方法一
    #读取正向提示词
    def onClick_buttonToText1(self):
        self.in1_content=self.textEdit1.toPlainText()
        print("已读入正向提示词："+self.in1_content)

        # 给label4设置文本,支持html的标签
        self.label4.setText("<font color=purpel>请在输入反向提示词后点击读入</font>")
        self.label4.repaint()


    # 定义槽方法二
    # 读取反向提示词
    def onClick_buttonToText2(self):
        self.in2_content = self.textEdit2.toPlainText()
        print("已读入反向提示词：" + self.in2_content)

        # 给label4设置文本,支持html的标签
        self.label4.setText("<font color=purpel>请点击生成</font>")
        self.label4.repaint()


    # 定义槽方法三
    # 生成最终图
    def onClick_ButtonToText3(self):
        # 调用文本框设置普通文本
        print("开始生成图片")
        # 给label4设置文本,支持html的标签
        self.label4.setText("<font color=purpel>正在生成图片</font>")
        self.label4.repaint()
        self.operator_work()


    # 定义槽方法四
    # 生成流程所需显示图片
    def onClick_buttonToText4(self):
        # 调用文本框设置HTML(富文本)
        self.fla = self.textEdit3.toPlainText()
        # print("最终结果如图")
        # a = int(input("需要哪一个阶段的图片？   输入0生成原图，输入1，2，3分别对应第一第二第三 三个阶段，输入4生成最终结果 请输入："))
        if self.fla == '0':
            img = Image.open(f'F:\\novelai-webui-aki-v2\\outputs\\txt2img-images\\{self.name1}')
            img.show()
        elif self.fla == '1':
            img = Image.open(f'F:\\novelai-webui-aki-v2\\outputs\\img2img-images\\{self.name2}')
            img.show()
        elif self.fla == '2':
            img = Image.open(f'F:\\novelai-webui-aki-v2\\outputs\\img2img-images\\{self.name3}')
            img.show()
        elif self.fla == '3':
            img = Image.open(f'F:\\novelai-webui-aki-v2\\outputs\\img2img-images\\{self.name4}')
            img.show()
        elif self.fla == '4':
            img = Image.open(f'F:\\novelai-webui-aki-v2\\outputs\\img2img-images\\{self.name5}')
            img.show()
        else:
            img = Image.open('D:\\GM3323D\\pencil4img.jpg')
            img.show()

    # 定义槽方法五
    # 确认对当前图片满意
    def onClick_buttonToText5(self):
        # # 给label4设置文本,支持html的标签
        # self.label4.setText("<font color=purpel>开始生成下一阶段图片</font>")
        # self.label4.repaint()

        # 找到生成操作按钮所在位置
        b_locator = '#txt2img_generate'
        button = get_button(self.shadow, b_locator)

        # 当前正处于生成效果图
        if self.f == 0:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>开始生成下一阶段图片</font>")
            self.label4.repaint()

            # 存储下满意的效果图的位置
            self.name1 = '0' + str(self.n - 1) + '.png'

            # 进入下一个生成页面，来生成图片的大致草图
            office.image.pencil4img(input_img=f'F:\\novelai-webui-aki-v2\outputs\\txt2img-images\\{self.name1}')

            # print("即将开始生成草图")

            # 找到进入下一个页面的按钮位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-139")'
            element = get_n_button(self.driver, js)

            # 点击按钮进入下一个页面
            get_nxt(element)

            # 清空输入框中的文字
            js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_prompt > label > textarea").value="";'
            clear(self.driver, js)

            # #输入正向提示词
            # in3_content = input('请输入正向标签: ')
            #
            # #输入反向提示词
            # in4_content = input('请输入反向标签: ')
            in3_content = '{rough sketch},monochrome,Tenebrism,'
            # 找到正向提示词所在的文本框
            t_in3_locator = '#img2img_prompt > label > textarea'
            txtbox = get_textbox(self.shadow, t_in3_locator)

            # 在正向提示词文本框中填充用户所需要的正向提示词
            input_words(txtbox, in3_content)

            # 等待2s
            sleep(2)

            # 找到反向提示词所在的文本框
            # t_in4_locator = '#img2img_neg_prompt > label > textarea'
            # txtbox = get_textbox(shadow,t_in4_locator)
            #
            # #在反向提示词文本框中填充用户所需要的反向提示词
            # input_words(txtbox,in4_content)

            # 找到重绘幅度得修改框得位置
            js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-242 > div.w-full.flex.flex-col > div > input").value="";'
            self.driver.execute_script(js)
            s_locator = '#component-242 > div.w-full.flex.flex-col > div > input'
            s_box = get_s_box(self.shadow, s_locator)

            # 对重绘幅度进行调整，这里取0.46
            # step = input('请输入重绘幅度: ')
            step = 0.3
            change_step(s_box, step)

            # n重置为0
            self.n = 0

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)

            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第一阶段的生成结果是否满意</font>")
            self.label4.repaint()

        elif self.f == 1:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>开始生成下一阶段图片</font>")
            self.label4.repaint()

            # 存储下满意的效果图的位置
            self.name2 = '0' + str(self.n - 1) + '.png'

            # 找到重绘幅度得修改框得位置
            js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-242 > div.w-full.flex.flex-col > div > input").value="";'
            self.driver.execute_script(js)
            s_locator = '#component-242 > div.w-full.flex.flex-col > div > input'
            s_box = get_s_box(self.shadow, s_locator)

            # 对重绘幅度进行调整，这里取0.46

            # step = input('请输入重绘幅度: ')
            step = 0.43
            change_step(s_box, step)

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)
            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第二阶段的生成结果是否满意</font>")
            self.label4.repaint()

        elif self.f == 2:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>开始生成下一阶段图片</font>")
            self.label4.repaint()

            # 存储下满意的效果图的位置
            self.name3 = '0' + str(self.n - 1) + '.png'

            # 找到重绘幅度得修改框得位置
            js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-242 > div.w-full.flex.flex-col > div > input").value="";'
            self.driver.execute_script(js)
            s_locator = '#component-242 > div.w-full.flex.flex-col > div > input'
            s_box = get_s_box(self.shadow, s_locator)

            # 对重绘幅度进行调整，这里取0.46
            # step = input('请输入重绘幅度: ')
            step = 0.46
            change_step(s_box, step)

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)
            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)
            # 找到图片存储的文件位置路径
            path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第三阶段的生成结果是否满意</font>")
            self.label4.repaint()

        elif self.f == 3:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>开始生成下一阶段图片</font>")
            self.label4.repaint()

            # 存储下满意的效果图的位置
            self.name4 = '0' + str(self.n - 1) + '.png'
            js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_prompt > label > textarea").value="";'

            # 清空文本框
            clear(self.driver, js)

            # 添加标签
            in3_content = 'spot color,greyscale,monochrome,'

            # 找到正向提示词所在的文本框
            t_in3_locator = '#img2img_prompt > label > textarea'
            txtbox = get_textbox(self.shadow, t_in3_locator)

            # 往文本框中填入提示词
            input_words(txtbox, in3_content)

            #等待两秒
            sleep(2)

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)

            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]  # os.sep添加系统分隔符

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第四阶段的生成结果是否满意</font>")
            self.label4.repaint()

        else:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>开始生成下一阶段图片</font>")
            self.label4.repaint()

            # 存储下满意的效果图的位置
            name5 = '0' + str(self.n - 1) + '.png'

            # 阶段四满意后显示最终草图
            img = Image.open('D:\\GM3323D\\pencil4img.jpg')
            img.show()

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>输入0生成原图，输入1，2，3，4分别对应第一、二、三、四 四个阶段，输入5生成最终结果 请输入：</font>")
            self.label4.repaint()

        # 修改f变量
        self.f += 1


    # 定义槽方法六
    # 确认对当前图片不满意
    def onClick_buttonToText6(self):

        # # 给label4设置文本,支持html的标签
        # self.label4.setText("<font color=purpel>重新生成图片中</font>")
        # self.label4.repaint()

        # 找到生成操作按钮所在位置
        b_locator = '#txt2img_generate'
        button = get_button(self.shadow, b_locator)

        if self.f == 0:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>重新生成图片中</font>")
            self.label4.repaint()

            # 按下操作按钮，进行生成操作
            generate(button)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F\novelai-webui-aki-v2\\outputs\\txt2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于这张图片是否满意</font>")
            self.label4.repaint()

        elif self.f == 1:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>重新生成图片中</font>")
            self.label4.repaint()

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)

            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第一阶段的生成结果是否满意</font>")
            self.label4.repaint()

        elif self.f == 2:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>重新生成图片中</font>")
            self.label4.repaint()

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)

            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第二阶段的生成结果是否满意</font>")
            self.label4.repaint()

        elif self.f == 3:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>重新生成图片中</font>")
            self.label4.repaint()

            # 找到重绘幅度得修改框的位置
            js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-242 > div.w-full.flex.flex-col > div > input").value="";'
            self.driver.execute_script(js)
            s_locator = '#component-242 > div.w-full.flex.flex-col > div > input'
            s_box = get_s_box(self.shadow, s_locator)

            # 对重绘幅度进行调整，这里取0.46
            # step = input('请输入重绘幅度: ')
            step = 0.46
            change_step(s_box, step)

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)

            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]  # os.sep添加系统分隔符

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第三阶段的生成结果是否满意</font>")
            self.label4.repaint()

        else:
            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>重新生成图片中</font>")
            self.label4.repaint()

            # 找到生成草图的按钮所在位置
            js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
            element = self.driver.execute_script(js)

            # 点击生成草图
            first_generate(element)

            # 等待10s内生成新的图片
            sleep(10)

            # 找到图片存储的文件位置路径
            path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            files = get_file_list(path)

            # 记录旧文件名
            # os.sep添加系统分隔符
            oldname = path + os.sep + files[self.n]  # os.sep添加系统分隔符

            # 设置新文件名
            newname = path + '\\0' + str(self.n) + '.png'

            # 用os模块中的rename方法对文件改名
            os.rename(oldname, newname)

            # 找到图片存储的文件位置路径
            new_path = path + '\\0' + str(self.n) + '.png'

            # 打开图片进行显示
            img = Image.open(new_path)
            img.show()

            # 修改下一次图片所在位置变量
            self.n += 1

            # 给label4设置文本,支持html的标签
            self.label4.setText("<font color=purpel>对于第四阶段的生成结果是否满意</font>")
            self.label4.repaint()



    #进行生成最终效果图
    def operator_work(self):
        # 选择Chrome浏览器
        self.driver = webdriver.Chrome()

        # 选择需要进入的网址，这里是项目所在的服务器位置
        url = 'http://127.0.0.1:7860'

        # 进入服务器所在网址
        get_url(url, self.driver)

        # 进行一段时间的登入等待，这里设置为60s
        time = 60
        wait(self.driver, time)

        # 找到服务器下shadow_root位置
        js = 'return document.querySelector("body > gradio-app").shadowRoot'
        self.shadow = get_shadow(self.driver, js)

        # 找到正向提示词所在的文本框
        t_in1_locator = '#txt2img_prompt > label > textarea'
        txtbox = get_textbox(self.shadow, t_in1_locator)

        # 在正向提示词文本框中填充用户所需要的正向提示词
        input_words(txtbox, self.in1_content)

        # 等待2s
        sleep(2)

        # 找到反向提示词所在的文本框
        t_in2_locator = '#txt2img_neg_prompt > label > textarea'
        txtbox = get_textbox(self.shadow, t_in2_locator)

        # 在反向提示词文本框中填充用户所需要的反向提示词
        input_words(txtbox, self.in2_content)

        # 找到生成操作按钮所在位置
        b_locator = '#txt2img_generate'
        button = get_button(self.shadow, b_locator)

        # 按下操作按钮，进行生成操作
        generate(button)

        # 等待10s内生成新的图片
        sleep(10)

        # 找到图片存储的文件位置路径
        path = 'F:\\novelai-webui-aki-v2\\outputs\\txt2img-images'
        files = get_file_list(path)

        # 记录旧文件名
        # os.sep添加系统分隔符
        oldname = path + os.sep + files[self.n]

        # 设置新文件名
        newname = path + '\\0' + str(self.n) + '.png'

        # 用os模块中的rename方法对文件改名
        os.rename(oldname, newname)

        # 找到图片存储的文件位置路径
        new_path = path + '\\0' + str(self.n) + '.png'

        #打开图片并显示
        img = Image.open(new_path)
        img.show()

        # 修改下一次图片所在位置变量
        self.n += 1

        # 给label4设置文本,支持html的标签
        self.label4.setText("<font color=purpel>对于这张生成结果是否满意</font>")
        self.label4.repaint()



        # self.f = 1
        # n = 0
        #
        # while f == 1:
        #
            # # 按下操作按钮，进行生成操作
            # generate(button)
            #
            # # 等待生成新的图片
            # sleep(10)
            # path = 'F:\\novelai-webui-aki-v2\\outputs\\txt2img-images'
            # files = get_file_list(path)
            #
            # oldname = path + os.sep + files[n]  # os.sep添加系统分隔符
            #
            # # 设置新文件名
            # newname = path + '\\0' + str(n) + '.png'
            #
            # os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
            # new_path = path + '\\0' + str(n) + '.png'
            # img = Image.open(new_path)
            # img.show()
            # n += 1
        #     inquire = input('你对本次生成结果满意吗：')
        #     if inquire == '满意':
        #         f = 0

        # name1 = '0' + str(self.n - 1) + '.png'
        # office.image.pencil4img(input_img=f'F:\\novelai-webui-aki-v2\outputs\\txt2img-images\\{name1}')
        # # 进入下一个生成页面，来生成图片的大致草图
        # print("即将开始生成草图")
        #
        # # 找到进入下一个页面的按钮位置
        # js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-139")'
        # element = get_n_button(self.driver, js)
        #
        # # 点击按钮进入下一个页面
        # get_nxt(element)
        #
        # # 清空输入框中的文字
        # js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_prompt > label > textarea").value="";'
        # clear(self.driver, js)
        #
        # # #输入正向提示词
        # # in3_content = input('请输入正向标签: ')
        # #
        # # #输入反向提示词
        # # in4_content = input('请输入反向标签: ')
        # in3_content = '{rough sketch},monochrome,Tenebrism,'
        # # 找到正向提示词所在的文本框
        # t_in3_locator = '#img2img_prompt > label > textarea'
        # txtbox = get_textbox(shadow, t_in3_locator)
        #
        # # 在正向提示词文本框中填充用户所需要的正向提示词
        # input_words(txtbox, in3_content)
        #
        # # 等待2s
        # sleep(2)
        #
        # # 找到反向提示词所在的文本框
        # # t_in4_locator = '#img2img_neg_prompt > label > textarea'
        # # txtbox = get_textbox(shadow,t_in4_locator)
        # #
        # # #在反向提示词文本框中填充用户所需要的反向提示词
        # # input_words(txtbox,in4_content)
        #
        # # 找到重绘幅度得修改框得位置
        # js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-242 > div.w-full.flex.flex-col > div > input").value="";'
        # self.driver.execute_script(js)
        # s_locator = '#component-242 > div.w-full.flex.flex-col > div > input'
        # s_box = get_s_box(shadow, s_locator)
        #
        # # 对重绘幅度进行调整，这里取0.46
        # # step = input('请输入重绘幅度: ')
        # step = 0.3
        # change_step(s_box, step)
        #
        # # 找到生成草图的按钮所在位置
        # js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
        # element = self.driver.execute_script(js)





        # f = 1
        # n = 0
        # while f == 1:

            # # 点击生成草图
            # first_generate(element)
            #
            # # 等待图形的生成
            # sleep(10)
            # path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            # files = get_file_list(path)
            # oldname = path + os.sep + files[n]  # os.sep添加系统分隔符
            #
            # # 设置新文件名
            # newname = path + '\\0' + str(n) + '.png'
            #
            # os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
            # new_path = path + '\\0' + str(n) + '.png'
            # img = Image.open(new_path)
            # img.show()
            # n += 1
            # inquire = input('你对第一阶段的生成结果满意吗：')
            # if inquire == '满意':
                # f = 0


        # name2 = '0' + str(self.n - 1) + '.png'
        #
        # # 找到重绘幅度得修改框得位置
        # js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-242 > div.w-full.flex.flex-col > div > input").value="";'
        # self.driver.execute_script(js)
        # s_locator = '#component-242 > div.w-full.flex.flex-col > div > input'
        # s_box = get_s_box(shadow, s_locator)
        #
        # # 对重绘幅度进行调整，这里取0.46
        #
        # # step = input('请输入重绘幅度: ')
        # step = 0.43
        # change_step(s_box, step)
        #
        # # 找到生成草图的按钮所在位置
        # js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
        # element = self.driver.execute_script(js)
        # f = 1
        #
        # while f == 1:

            # # 点击生成草图
            # first_generate(element)
            #
            # # 等待图形的生成
            # sleep(10)
            # path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
            # files = get_file_list(path)
            # oldname = path + os.sep + files[self.n]  # os.sep添加系统分隔符
            #
            # # 设置新文件名
            # newname = path + '\\0' + str(self.n) + '.png'
            #
            # os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
            # new_path = path + '\\0' + str(self.n) + '.png'
            # img = Image.open(new_path)
            # img.show()
            # self.n += 1
            # inquire = input('你对第二阶段的生成结果满意吗：')
            # if inquire == '满意':
            #     f = 0

        # self.name3 = '0' + str(self.n - 1) + '.png'
        #
        # # 找到重绘幅度得修改框得位置
        # js = 'document.querySelector("body > gradio-app").shadowRoot.querySelector("#component-242 > div.w-full.flex.flex-col > div > input").value="";'
        # self.driver.execute_script(js)
        # s_locator = '#component-242 > div.w-full.flex.flex-col > div > input'
        # s_box = get_s_box(shadow, s_locator)
        #
        # # 对重绘幅度进行调整，这里取0.46
        # # step = input('请输入重绘幅度: ')
        # step = 0.46
        # change_step(s_box, step)
        #
        # # 找到生成草图的按钮所在位置
        # js = 'return document.querySelector("body > gradio-app").shadowRoot.querySelector("#img2img_generate")'
        # element = self.driver.execute_script(js)
        # f = 1
        #
        # while f == 1:
        #
        #     # 点击生成草图
        #     first_generate(element)
        #
        #     # 等待图形的生成
        #     sleep(10)
        #     path = 'F:\\novelai-webui-aki-v2\\outputs\\img2img-images'
        #     files = get_file_list(path)
        #     oldname = path + os.sep + files[n]  # os.sep添加系统分隔符
        #
        #     # 设置新文件名
        #     newname = path + '\\0' + str(n) + '.png'
        #
        #     os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
        #     new_path = path + '\\0' + str(n) + '.png'
        #     img = Image.open(new_path)
        #     img.show()
        #     n += 1
        #     inquire = input('你对第三阶段的生成结果满意吗：')
        #     if inquire == '满意':
        #         f = 0

        # self.name4 = '0' + str(n - 1) + '.png'
        # img = Image.open('D:\\GM3323D\\pencil4img.jpg')
        # img.show()



  # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)

    # 设置图标
    # app.setWindowIcon(QIcon('images/001.jpg'))

    # 创建对象
    main = QTextEditDemo()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())

