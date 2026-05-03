"""
安全校验子模块 (AGENT-EXEC)
负责校验指令安全性，拦截高危操作
"""
from typing import Tuple, List
from common import Command, CommandType, Point, Config


class SafetyChecker:
    def __init__(self):
        self.enable_check = Config.ENABLE_SAFETY_CHECK
        # 高危操作关键词黑名单
        self.dangerous_keywords = [
            "delete", "del", "remove", "rm",
            "format", "fdisk", "diskpart",
            "regedit", "registry",
            "chmod", "chown", "permission",
            "shutdown", "reboot", "restart",
            "taskkill", "kill", "process",
            "write", "overwrite",
            "system32", "windows\\system32"
        ]

    def check(self, command: Command, screen_width: int, screen_height: int) -> Tuple[bool, str]:
        """
        校验指令安全性
        :param command: 要执行的指令
        :param screen_width: 屏幕宽度
        :param screen_height: 屏幕高度
        :return: (是否安全, 错误信息)
        """
        if not self.enable_check:
            return True, ""
            
        # 检查坐标是否在屏幕范围内
        if command.type == CommandType.CLICK and command.target:
            if not self._is_point_in_screen(command.target, screen_width, screen_height):
                return False, "坐标超出屏幕范围"
        
        # 检查等待时间是否合理
        if command.type == CommandType.WAIT and command.wait_time:
            if command.wait_time > 600:  # 最大等待10分钟
                return False, "等待时间过长"
        
        return True, ""

    def check_command_str(self, command_str: str) -> Tuple[bool, str]:
        """
        直接校验指令字符串的安全性
        """
        if not self.enable_check:
            return True, ""
            
        lower_str = command_str.lower()
        for keyword in self.dangerous_keywords:
            if keyword in lower_str:
                return False, f"检测到高危操作关键词: {keyword}"
        
        return True, ""

    def _is_point_in_screen(self, point: Point, width: int, height: int) -> bool:
        """检查点是否在屏幕范围内"""
        return 0 <= point.x <= width and 0 <= point.y <= height
