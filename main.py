#!/usr/bin/env python3
"""
Kaelo 桌面视觉自动化系统 - 主程序入口
"""
import time
import signal
import sys
from typing import Optional
import click
from agent_screen import ScreenCapture, ElementDetector
from agent_comm import Communicator
from agent_exec import CommandParser, SafetyChecker, ActionExecutor
from common import Config, CommandType


ASCII_ART = """
 ██ ▄█▀ ▄▄▄       ██▓███   ██▓███  
 ██▄█▒ ▒████▄    ▓██░  ██▒▓██░  ██▒
▓███▄░ ▒██  ▀█▄  ▓██░ ██▓▒▓██░ ██▓▒
▓██ █▄ ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒██▄█▓▒ ▒
▒██▒ █▄ ▓█   ▓██▒▒██▒ ░  ░▒██▒ ░  ░
▒ ▒▒ ▓▒ ▒▒   ▓▒█░▒▓▒░ ░  ░▒▓▒░ ░  ░
░ ░▒ ▒  ▒   ▒▒ ░░▒ ░     ░▒ ░     
░ ░  ░  ░   ▒   ░░       ░░        
        ░                         
"""


def print_welcome():
    """打印欢迎界面"""
    print(ASCII_ART)
    print("=" * 50)
    print("Kaelo - 桌面视觉自动化系统")
    print("轻量级 · 智能化 · 安全可靠")
    print("=" * 50)
    print()


class KaeloAutomation:
    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.element_detector = ElementDetector()
        self.communicator = Communicator()
        self.command_parser = CommandParser()
        self.safety_checker = SafetyChecker()
        self.action_executor = ActionExecutor()
        self.running = False
        self.consecutive_errors = 0
        self.max_consecutive_errors = 5
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """处理中断信号"""
        print("\n\n🛑 收到中断信号，正在停止...")
        self.running = False

    def run(self, user_request: str):
        """
        运行主循环
        """
        print_welcome()
        print(f"🎯 用户需求: {user_request}")
        print()
        
        self.running = True
        history = []
        
        try:
            while self.running:
                try:
                    # 1. 屏幕捕获
                    print("📸 [1/5] 正在捕获屏幕...")
                    image = self.screen_capture.capture_pil()
                    if image is None:
                        print("⚠️  屏幕捕获失败，重试...")
                        self.consecutive_errors += 1
                        if self.consecutive_errors >= self.max_consecutive_errors:
                            print(f"❌ 连续失败 {self.max_consecutive_errors} 次，停止运行")
                            break
                        time.sleep(1)
                        continue
                    
                    # 2. 元素识别
                    print("🔍 [2/5] 正在识别可交互元素...")
                    image_np = __import__('numpy').array(image)
                    try:
                        elements = self.element_detector.detect(image_np)
                        print(f"✅ 检测到 {len(elements)} 个元素")
                    except Exception as e:
                        print(f"⚠️  元素识别失败: {e}")
                        self.consecutive_errors += 1
                        if self.consecutive_errors >= self.max_consecutive_errors:
                            print(f"❌ 连续失败 {self.max_consecutive_errors} 次，停止运行")
                            break
                        time.sleep(1)
                        continue
                    
                    # 3. AI 决策
                    print("🤖 [3/5] 正在请求 AI 决策...")
                    ai_response = self.communicator.send_request(
                        image, elements, user_request, history
                    )
                    if ai_response is None:
                        print("⚠️  AI 请求失败，重试...")
                        self.consecutive_errors += 1
                        if self.consecutive_errors >= self.max_consecutive_errors:
                            print(f"❌ 连续失败 {self.max_consecutive_errors} 次，停止运行")
                            break
                        time.sleep(1)
                        continue
                    
                    # 检查是否有多个指令或空指令
                    ai_response = ai_response.strip()
                    if not ai_response:
                        print("❌ AI 返回空指令，停止运行")
                        break
                    if '\n' in ai_response or len(ai_response.split(';')) > 1:
                        print("❌ AI 返回多条指令，停止运行")
                        break
                    
                    print(f"💬 AI 响应: {ai_response}")
                    
                    # 3.5 安全校验 - 指令字符串
                    safe, msg = self.safety_checker.check_command_str(ai_response)
                    if not safe:
                        print(f"⛔ 安全检查失败: {msg}")
                        break
                    
                    # 4. 指令解析
                    print("📝 [4/5] 正在解析指令...")
                    command = self.command_parser.parse(ai_response)
                    if command is None:
                        print("⚠️  指令解析失败")
                        self.consecutive_errors += 1
                        if self.consecutive_errors >= self.max_consecutive_errors:
                            print(f"❌ 连续失败 {self.max_consecutive_errors} 次，停止运行")
                            break
                        time.sleep(1)
                        continue
                    
                    # 4.5 安全校验 - 坐标等
                    screen_width, screen_height = self.action_executor.get_screen_size()
                    safe, msg = self.safety_checker.check(command, screen_width, screen_height)
                    if not safe:
                        print(f"⛔ 安全检查失败: {msg}")
                        break
                    
                    # 5. 执行操作
                    print("🎮 [5/5] 正在执行操作...")
                    if command.type == CommandType.END:
                        print("\n✨ 任务完成！")
                        break
                    
                    try:
                        success = self.action_executor.execute(command)
                        if not success:
                            print("⚠️  操作执行失败")
                            self.consecutive_errors += 1
                            if self.consecutive_errors >= self.max_consecutive_errors:
                                print(f"❌ 连续失败 {self.max_consecutive_errors} 次，停止运行")
                                break
                            time.sleep(1)
                            continue
                    except Exception as e:
                        print(f"❌ 执行操作时出错: {e}")
                        print("⚠️  操作可能被系统拦截，停止运行")
                        break
                    
                    # 重置错误计数
                    self.consecutive_errors = 0
                    
                    # 更新历史记录
                    history.append({"role": "assistant", "content": ai_response})
                    
                    print()
                    # 等待下一循环
                    time.sleep(Config.SCREEN_CAPTURE_DELAY)
                    
                except Exception as e:
                    print(f"⚠️  循环内部出错: {e}")
                    self.consecutive_errors += 1
                    if self.consecutive_errors >= self.max_consecutive_errors:
                        print(f"❌ 连续失败 {self.max_consecutive_errors} 次，停止运行")
                        break
                    time.sleep(1)
                    
        except Exception as e:
            print(f"❌ 系统出错: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """清理资源"""
        print("\n🧹 正在清理资源...")
        try:
            self.screen_capture.cleanup()
        except:
            pass
        print("👋 再见！")


@click.command()
@click.argument('request')
@click.version_option(version='1.0.0', prog_name='kaelo')
def main(request):
    """
    Kaelo 桌面视觉自动化系统
    
    REQUEST: 用户的自动化需求描述
    
    示例:
      kaelo "打开计算器"
      kaelo "打开记事本并输入 Hello World"
    """
    try:
        automation = KaeloAutomation()
        automation.run(request)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
