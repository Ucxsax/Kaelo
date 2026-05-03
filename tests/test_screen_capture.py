"""
屏幕捕获模块测试
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_screen import ScreenCapture


def test_capture():
    print("测试屏幕捕获...")
    sc = ScreenCapture()
    
    try:
        # 测试 numpy 数组方式
        img_np = sc.capture()
        if img_np is not None:
            print(f"✅ 捕获成功！图像尺寸: {img_np.shape}")
        else:
            print("❌ 捕获失败")
        
        # 测试 PIL Image 方式
        img_pil = sc.capture_pil()
        if img_pil is not None:
            print(f"✅ PIL Image 捕获成功！尺寸: {img_pil.size}")
        else:
            print("❌ PIL Image 捕获失败")
            
    finally:
        sc.cleanup()


if __name__ == "__main__":
    test_capture()
