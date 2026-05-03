"""
操作执行子模块 (AGENT-EXEC)
负责调用键鼠接口执行实际操作
"""
import time
import pyautogui
from typing import Optional
from common import Command, CommandType


class ActionExecutor:
    def __init__(self):
        # 设置安全措施
        pyautogui.FAILSAFE = True  # 鼠标移动到左上角会紧急停止
        pyautogui.PAUSE = 0.5  # 每个操作之间间隔0.5秒

    def execute(self, command: Command) -> bool:
        """
        执行指令
        :param command: 要执行的指令
        :return: 是否执行成功
        """
        try:
            if command.type == CommandType.CLICK and command.target:
                self._click(command.target.x, command.target.y)
            elif command.type == CommandType.WAIT and command.wait_time:
                self._wait(command.wait_time)
            elif command.type == CommandType.END:
                return True
            return True
        except Exception as e:
            print(f"执行操作失败: {e}")
            return False

    def _click(self, x: int, y: int):
        """执行点击操作"""
        print(f"执行点击: ({x}, {y})")
        pyautogui.click(x, y)

    def _wait(self, seconds: float):
        """执行等待操作"""
        print(f"等待 {seconds} 秒")
        time.sleep(seconds)

    def get_screen_size(self) -> tuple:
        """获取屏幕尺寸"""
        return pyautogui.size()
