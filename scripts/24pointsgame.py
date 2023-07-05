#24 points game
#Please install pip install pyautogui first, pip install pyperclip
#If using the ubuntu system, you also need to install sudo apt-get install xclip
#24点游戏
#请先安装pip install pyautogui,pip install pyperclip
#如果使用ubuntu系统，还需要安装sudo apt-get install xclip

import pyautogui
import pyperclip
import random
import time

def replace_start(string, replacement, num_chars):
    replaced_string = replacement + string[num_chars:]
    return replaced_string

def replace_all(string, target_char, replacement_chars):
    replaced_string = string
    replaced_string = replaced_string.replace(target_char, replacement_chars)
    return replaced_string


def remove_trailing_char(string, char):
    if string.endswith(char):
        return string[:-len(char)]
    else:
        return string

def calculate_24(nums, expression=""):
    if 3 in numbers and 8 in numbers:
    	new_nums = numbers.copy()
    	new_nums.remove(3)
    	new_nums.remove(8)

    	if new_nums == [3,8] or new_nums == [8,3]:
                output = f'24点游戏！\n题目：{numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}。'
                pyperclip.copy(output)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                time.sleep(3)
                output = f'解：先算(8 / 3) 再算 3 - (8 / 3) 再算 8 / ( 1/3 ) '
                time.sleep(3)
                pyperclip.copy(output)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                return True


    if len(nums) == 1:
        if nums[0] == 24:
            output = f'24点游戏！\n题目：{numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}。'
            pyperclip.copy(output)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(3)

            original_string = expression
            replacement = "先算: "
            num_chars = 3
            original_string = replace_start(original_string, replacement, num_chars)
            replacement_chars = f" 再算: "
            target_char = ")"
            original_string = replace_all(original_string, target_char, replacement_chars)
            char_to_remove = " 再算: "
            new_string = remove_trailing_char(original_string, char_to_remove)
            output = f'解：{new_string}'
            time.sleep(3)
            pyperclip.copy(output)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            return True
        else:
            return False

    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j:
                new_nums = [nums[k] for k in range(len(nums)) if k != i and k != j]
                if calculate_24(new_nums + [nums[i] + nums[j]], "(" + expression + str(nums[i]) + " + " + str(nums[j]) + ")"):
                    return True
                
                if calculate_24(new_nums + [nums[i] - nums[j]], "(" + expression + str(nums[i]) + " - " + str(nums[j]) + ")"):
                    return True
                
                if calculate_24(new_nums + [nums[i] * nums[j]], "(" + expression + str(nums[i]) + " * " + str(nums[j]) + ")"):
                    return True
             
                if nums[j] != 0:
                    if calculate_24(new_nums + [nums[i] / nums[j]], "(" + expression + str(nums[i]) + " / " + str(nums[j]) + ")"):
                        return True

    return False

if __name__ == '__main__':
    time.sleep(3)
    pyautogui.click()
    while 1:
        numbers = [int(random.randint(1,13)), int(random.randint(1,13)), int(random.randint(1,13)), int(random.randint(1,13))]
        if calculate_24(numbers):
            time.sleep(6)


