"""
Windows 环境适配测试
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import platform


def test_windows_environment():
    print("Windows 环境适配测试...")
    print(f"操作系统: {platform.system()} {platform.release()}")
    
    # 检查是否是 Windows 系统
    if platform.system() != "Windows":
        print("❌ 非 Windows 系统")
        return False
    
    print(f"✅ Windows 系统检测通过: {platform.platform()}")
    
    # 检查 Python 版本
    print(f"Python 版本: {sys.version}")
    
    # 检查关键依赖的导入
    print("\n检查依赖库:")
    try:
        import mss
        print("✅ mss 导入成功")
    except Exception as e:
        print(f"❌ mss 导入失败: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow 导入成功")
    except Exception as e:
        print(f"❌ Pillow 导入失败: {e}")
        return False
    
    try:
        import cv2
        print("✅ opencv-python 导入成功")
    except Exception as e:
        print(f"❌ opencv-python 导入失败: {e}")
        return False
    
    try:
        import numpy
        print("✅ numpy 导入成功")
    except Exception as e:
        print(f"❌ numpy 导入失败: {e}")
        return False
    
    try:
        import pyautogui
        print("✅ pyautogui 导入成功")
        # 检查屏幕尺寸获取
        screen_width, screen_height = pyautogui.size()
        print(f"   屏幕尺寸: {screen_width}x{screen_height}")
    except Exception as e:
        print(f"❌ pyautogui 导入失败: {e}")
        return False
    
    try:
        import openai
        print("✅ openai 导入成功")
    except Exception as e:
        print(f"❌ openai 导入失败: {e}")
        return False
    
    try:
        import click
        print("✅ click 导入成功")
    except Exception as e:
        print(f"❌ click 导入失败: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 导入成功")
    except Exception as e:
        print(f"❌ python-dotenv 导入失败: {e}")
        return False
    
    print("\n✅ 所有依赖检查通过！")
    return True


if __name__ == "__main__":
    test_windows_environment()
