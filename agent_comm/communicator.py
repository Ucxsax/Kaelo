"""
通信模块 (AGENT-COMM)
负责数据打包、转发和指令校验
支持 OpenAI API 和 Ollama
"""
import time
from typing import Optional, List
from PIL import Image
import base64
import io
from openai import OpenAI
from common import Config, Element, Command, CommandType


class Communicator:
    def __init__(self):
        # 根据配置选择 AI 服务
        self.ai_service = Config.AI_SERVICE.lower()
        
        if self.ai_service == "ollama":
            print("🤖 使用 Ollama 本地模型")
            try:
                import ollama
                self.ollama_client = ollama.Client(host=Config.OLLAMA_BASE_URL.replace("/v1", ""))
                self.model = Config.OLLAMA_MODEL
            except ImportError:
                raise ImportError("请先安装 Ollama 库: pip install ollama")
        else:
            print("🤖 使用 OpenAI API")
            self.client = OpenAI(
                api_key=Config.OPENAI_API_KEY,
                base_url=Config.OPENAI_BASE_URL
            )
            self.model = Config.OPENAI_MODEL
        
        self.max_retries = Config.MAX_RETRY_ATTEMPTS

    def image_to_base64(self, image: Image.Image) -> str:
        """将 PIL Image 转换为 base64 字符串"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def send_request(
        self,
        image: Image.Image,
        elements: List[Element],
        user_request: str,
        history: Optional[List] = None
    ) -> Optional[str]:
        """
        发送请求给 AI
        :param image: 屏幕截图
        :param elements: 元素列表
        :param user_request: 用户原始需求
        :param history: 历史操作记录
        :return: AI 响应字符串，失败返回 None
        """
        for attempt in range(self.max_retries):
            try:
                base64_image = self.image_to_base64(image)
                
                elements_desc = "\n".join([
                    f"- {e.type} at ({e.rect.x}, {e.rect.y}), size {e.rect.width}x{e.rect.height}, name={e.name}"
                    for e in elements
                ])
                
                system_prompt = """你是一个桌面自动化助手。你的任务是根据屏幕截图、元素列表和用户需求，生成下一步操作指令。

只支持以下三种指令：
1. click x y - 点击屏幕坐标 (x,y) 处
2. wait t - 等待 t 秒
3. end - 任务完成，停止自动化

输出格式：只输出纯指令内容，不要有任何解释。每次只输出一条指令。
不要执行任何危险操作，如删除文件、修改系统配置等。"""

                user_content = f"用户需求：{user_request}\n\n检测到的元素：\n{elements_desc}"
                
                if self.ai_service == "ollama":
                    # 使用 Ollama 原生 API
                    import ollama
                    response = self.ollama_client.generate(
                        model=self.model,
                        prompt=f"{system_prompt}\n\n{user_content}",
                        images=[base64_image],
                        options={
                            "temperature": 0.3,
                            "num_predict": 100
                        }
                    )
                    return response["response"].strip()
                else:
                    # 使用 OpenAI API
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_content},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                            ]
                        }
                    ]
                    
                    if history:
                        messages = history + messages
                    
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=100,
                        temperature=0.3
                    )
                    return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"通信失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
        return None

    def validate_command(self, command_str: str) -> bool:
        """
        校验 AI 返回的指令格式是否有效
        """
        if not command_str:
            return False
        parts = command_str.strip().split()
        if not parts:
            return False
        cmd = parts[0].lower()
        if cmd not in ["click", "wait", "end"]:
            return False
        if cmd == "click" and len(parts) < 3:
            return False
        if cmd == "wait" and len(parts) < 2:
            return False
        return True
