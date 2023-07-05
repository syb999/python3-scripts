#Automatically execute chicken with rabbit cage questioning.
#Please install pip install pyautogui first, pip install pyperclip
#If using the ubuntu system, you also need to install sudo apt-get install xclip
#自动执行鸡兔同笼提问。
#请先安装pip install pyautogui,pip install pyperclip
#如果使用ubuntu系统，还需要安装sudo apt-get install xclip

import pyautogui
import time
import random
import pyperclip

def chicken_rabbit(total_heads):
    chicken_count = int(random.randint(0,total_heads))
    rabbit_count = total_heads - chicken_count
    total_legs = 2 * chicken_count + 4 * rabbit_count
    return [total_legs, chicken_count, rabbit_count]

def quest():
    total_heads = int(random.randint(2,200))
    reslut = chicken_rabbit(total_heads)
    total_legs = str(reslut[0])
    chicken_count = str(reslut[1])
    rabbit_count = str(reslut[2])
    person_list = ["金", "凯莉", "紫堂幻", "格瑞", "嘉德罗斯", "雷德", \
    "蒙特祖玛", "银爵", "安迷修", "蕾蒂", "蕾蒂妹妹", "鬼狐天冲", "莱娜", \
    "艾比", "埃米", "雷狮", "卡米尔", "佩利", "帕格斯", "秋", "小黑洞", \
    "安莉洁", "神近耀", "丹尼尔"]
    random_person = random.choice(person_list)
    output = f"题目：{random_person}的家里养了一些鸡和兔子，同时养在一个笼子里。\
{random_person}数了数，它们共有{total_heads}个头，{total_legs}个脚。\
\n问：{random_person}家养的鸡和兔各有多少只？"
    pyperclip.copy(output)
    return [chicken_count, rabbit_count]
 

def _output():
    result = quest()
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(6)
    output = f"答案：{result[0]}只鸡,{result[1]}只兔。"
    pyperclip.copy(output)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    
if __name__ == '__main__':
    time.sleep(2)  # 等待2秒钟，确保您有足够的时间将焦点切换到文本输入区域
    pyautogui.click()  # 单击以确保焦点在正确的位置
    while 1:
        _output()
    
