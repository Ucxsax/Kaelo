"""
安全校验模块测试
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_exec import SafetyChecker, CommandParser
from common import CommandType


def test_safety():
    print("安全校验模块测试...")
    checker = SafetyChecker()
    parser = CommandParser()
    
    # 测试危险指令
    dangerous_cmds = [
        "delete something",
        "format C:",
        "regedit",
        "chmod 777",
        "shutdown /s",
        "taskkill /f",
        "write to C:\\windows\\system32",
    ]
    
    print("\n测试危险指令检测:")
    all_pass = True
    for cmd in dangerous_cmds:
        safe, msg = checker.check_command_str(cmd)
        if not safe:
            print(f"✅ '{cmd}' -> 正确拒绝: {msg}")
        else:
            print(f"❌ '{cmd}' -> 未被检测到")
            all_pass = False
    
    # 测试安全指令
    safe_cmds = [
        "click 100 200",
        "wait 3",
        "end",
    ]
    
    print("\n测试安全指令:")
    for cmd in safe_cmds:
        safe, msg = checker.check_command_str(cmd)
        if safe:
            print(f"✅ '{cmd}' -> 允许通过")
        else:
            print(f"❌ '{cmd}' -> 误报: {msg}")
            all_pass = False
    
    # 测试坐标越界
    print("\n测试坐标越界:")
    test_cases = [
        ("click 100 200", 1920, 1080, True),  # 正常
        ("click -10 200", 1920, 1080, False),  # X 负
        ("click 100 -20", 1920, 1080, False),  # Y 负
        ("click 3000 200", 1920, 1080, False),  # X 超界
        ("click 100 2000", 1920, 1080, False),  # Y 超界
    ]
    
    for cmd_str, screen_w, screen_h, expected_safe in test_cases:
        cmd = parser.parse(cmd_str)
        if cmd:
            safe, msg = checker.check(cmd, screen_w, screen_h)
            if safe == expected_safe:
                print(f"✅ '{cmd_str}' -> {'安全' if safe else '危险'} (期望 {'安全' if expected_safe else '危险'})")
            else:
                print(f"❌ '{cmd_str}' -> {'安全' if safe else '危险'}, 期望 {'安全' if expected_safe else '危险'}")
                all_pass = False
    
    print(f"\n整体: {'✅ 通过' if all_pass else '❌ 失败'}")
    return all_pass


if __name__ == "__main__":
    test_safety()
