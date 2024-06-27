import time
import hiwonder.Board as Board

print('''
----------------------------------------------------------
以下指令均需在LX终端使用，LX终端可通过ctrl+alt+t打开，或点
击上栏的黑色LX终端图标。
----------------------------------------------------------
Usage:
    python3 BuzzerControlDemo.py
----------------------------------------------------------
Version: --V1.2  2021/07/03
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

Board.setBuzzer(0) # 关闭

Board.setBuzzer(1) # 打开
time.sleep(0.1) # 延时
Board.setBuzzer(0) #关闭

time.sleep(1) # 延时

Board.setBuzzer(1)
time.sleep(0.5)
Board.setBuzzer(0)