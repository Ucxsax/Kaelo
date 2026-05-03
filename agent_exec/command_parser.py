"""
指令解析子模块 (AGENT-EXEC)
负责解析 AI 返回的指令
"""
from typing import Optional
from common import Command, CommandType, Point


class CommandParser:
    def parse(self, command_str: str) -> Optional[Command]:
        """
        解析指令字符串为 Command 对象
        :param command_str: AI 返回的指令字符串
        :return: Command 对象，解析失败返回 None
        """
        if not command_str:
            return None
            
        parts = command_str.strip().split()
        if not parts:
            return None
            
        cmd_type = parts[0].lower()
        
        try:
            if cmd_type == "click":
                if len(parts) < 3:
                    return None
                x = int(parts[1])
                y = int(parts[2])
                return Command(
                    type=CommandType.CLICK,
                    target=Point(x=x, y=y)
                )
            elif cmd_type == "wait":
                if len(parts) < 2:
                    return None
                wait_time = float(parts[1])
                return Command(
                    type=CommandType.WAIT,
                    wait_time=wait_time
                )
            elif cmd_type == "end":
                return Command(
                    type=CommandType.END
                )
            else:
                return None
        except ValueError:
            return None
