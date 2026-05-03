"""
指令解析模块测试
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_exec import CommandParser
from common import CommandType


def test_parse():
    print("测试指令解析...")
    parser = CommandParser()
    
    test_cases = [
        ("click 100 200", CommandType.CLICK),
        ("wait 3.5", CommandType.WAIT),
        ("end", CommandType.END),
        ("invalid cmd", None),
        ("click onlyone", None),
        ("wait notanumber", None),
    ]
    
    all_pass = True
    for cmd_str, expected_type in test_cases:
        cmd = parser.parse(cmd_str)
        if cmd is None and expected_type is None:
            print(f"✅ '{cmd_str}' -> 正确拒绝")
        elif cmd is not None and cmd.type == expected_type:
            print(f"✅ '{cmd_str}' -> {cmd.type}")
        else:
            print(f"❌ '{cmd_str}' -> 解析错误 (期望 {expected_type}, 得到 {cmd.type if cmd else None})")
            all_pass = False
    
    print(f"\n整体: {'✅ 通过' if all_pass else '❌ 失败'}")


if __name__ == "__main__":
    test_parse()
