"""
屏幕捕获模块 (AGENT-SCREEN)
负责实时截取屏幕画面
"""
import time
from typing import Optional
import mss
import numpy as np
from PIL import Image
from common import Config


class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
        self.max_retries = Config.MAX_RETRY_ATTEMPTS

    def capture(self, monitor: int = 0) -> Optional[np.ndarray]:
        """
        截取屏幕画面
        :param monitor: 显示器编号 (0 表示主显示器)
        :return: 截图的 numpy 数组，失败返回 None
        """
        for attempt in range(self.max_retries):
            try:
                monitor_info = self.sct.monitors[monitor]
                screenshot = self.sct.grab(monitor_info)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                return np.array(img)
            except Exception as e:
                print(f"屏幕捕获失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(0.5)
        return None

    def capture_pil(self, monitor: int = 0) -> Optional[Image.Image]:
        """
        截取屏幕并返回 PIL Image 对象
        """
        img_array = self.capture(monitor)
        if img_array is not None:
            return Image.fromarray(img_array)
        return None

    def cleanup(self):
        """清理资源"""
        self.sct.close()
