"""
元素识别模块 (AGENT-SCREEN)
负责识别可交互元素并生成坐标
"""
from typing import List
import numpy as np
import cv2
from common import Element, Rect, Point


class ElementDetector:
    def __init__(self):
        pass

    def detect(self, image: np.ndarray) -> List[Element]:
        """
        检测可交互元素
        :param image: 输入图像
        :return: 检测到的元素列表
        """
        if image is None or len(image.shape) < 2:
            return []
            
        elements = []
        
        try:
            # 使用边缘检测识别可能的可交互元素
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # 高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Canny边缘检测
            edges = cv2.Canny(blurred, 50, 150)
            
            # 找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            img_height, img_width = image.shape[:2]
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # 过滤太小的区域
                if w < 20 or h < 20:
                    continue
                if w > img_width * 0.9 or h > img_height * 0.9:
                    continue
                    
                rect = Rect(x=x, y=y, width=w, height=h)
                element = Element(
                    type="unknown",
                    rect=rect,
                    name=None,
                    text=None
                )
                elements.append(element)
                
        except Exception as e:
            print(f"元素识别出错: {e}")
            # 返回空列表而不是抛出异常
            
        return elements
