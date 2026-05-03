# Kaelo 快速开始指南

## 项目简介
Kaelo 是一个轻量级桌面视觉自动化系统，通过 AI 智能体理解屏幕内容并执行自动化操作。

## 前置要求
- Windows 10 或 Windows 11
- Python 3.8+
- **二选一**：
  - OpenAI API Key (或兼容 API)
  - 或 Ollama（本地运行免费模型）

---

## ⚡ 快速安装（推荐）

### 方式一：开发者模式（当前使用）

```bash
# 1. 进入项目目录
cd e:\Kaelo

# 2. （可选）创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 3. 以可编辑模式安装项目
pip install -e .

# 4. 配置 API Key
copy .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

然后就可以直接使用 `kaelo` 命令了！

---

## 📦 安装详细步骤

### 1. 克隆/下载项目
```bash
cd e:\Kaelo
```

### 2. 创建虚拟环境 (推荐)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安装项目
```bash
# 方式 A：以可编辑模式安装（推荐用于开发）
pip install -e .

# 方式 B：普通安装
pip install .
```

### 4. 配置环境变量
复制 `.env.example` 为 `.env`：
```bash
copy .env.example .env
```

#### 配置选项一：使用 OpenAI API
编辑 `.env` 文件：
```env
AI_SERVICE=openai
OPENAI_API_KEY=你的_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```

#### 配置选项二：使用 Ollama（免费本地）
1. 首先下载安装 Ollama：https://ollama.com/
2. 下载一个视觉模型（支持图像识别的模型）：
   ```bash
   ollama pull llama3.2
   # 或其他支持视觉的模型：qwen2.5, minicpm-v 等
   ```
3. 编辑 `.env` 文件：
```env
AI_SERVICE=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2
```

---

## 🚀 使用方法

### 基本用法

```bash
# 直接使用 kaelo 命令！
kaelo "你的自动化需求"
```

### 实用示例

```bash
# 打开计算器
kaelo "打开 Windows 计算器"

# 打开记事本
kaelo "打开记事本并输入 Hello World"

# 简单点击操作
kaelo "点击开始按钮"
```

### 查看帮助

```bash
kaelo --help
```

### 查看版本

```bash
kaelo --version
```

---

## 🧪 运行测试

在正式使用前，运行测试检查环境：

```bash
# 检查 Windows 环境
python tests\test_windows.py

# 检查屏幕捕获
python tests\test_screen_capture.py

# 检查指令解析
python tests\test_command_parser.py

# 检查安全校验
python tests\test_safety.py
```

---

## 🔧 其他启动方式

如果不安装，也可以直接运行：

```bash
python main.py "你的需求"
```

---

## ⚙️ 工作原理

Kaelo 的执行流程：

1. 📸 **屏幕捕获** - 实时截取当前屏幕
2. 🔍 **元素识别** - 识别可交互元素和坐标
3. 🤖 **AI 决策** - 发送给 AI 分析并生成指令
4. 📝 **指令解析** - 解析 AI 返回的指令
5. 🛡️ **安全校验** - 检查是否包含危险操作
6. 🎮 **操作执行** - 执行点击、等待等操作
7. 🔄 **循环** - 重复以上步骤直到任务完成

---

## 🛡️ 安全说明

Kaelo 内置安全校验机制，拒绝以下类型的操作：
- 修改注册表
- 修改系统环境变量
- 格式化磁盘
- 删除系统文件
- 篡改系统权限
- 启动/终止系统进程
- 写入/读取敏感文件

⚠️ **重要提示**：
- Kaelo 仅供学习和个人使用
- 禁止用于恶意操作
- 所有操作基于实时屏幕画面判定
- 单步执行模式，复杂任务分步执行

---

## ⌨️ 快捷键

- **Ctrl + C** - 在运行中安全停止

---

## 🐛 故障排查

### 屏幕捕获失败
- 确保以管理员权限运行？不需要，但要确保有屏幕访问权限
- 检查是否有其他程序拦截屏幕捕获

### AI 调用失败
- 检查 API Key 是否正确配置
- 检查网络连接
- 检查 API 额度是否充足
- 尝试更换 API 服务地址

### 操作执行失败
- 检查是否有其他程序弹窗干扰
- 检查屏幕分辨率是否变化
- 确认点击坐标是否在有效范围内

### 'kaelo' 命令不可用
- 确保已正确安装项目：`pip install -e .`
- 检查是否在正确的虚拟环境中
- 尝试重新打开终端

---

## 📁 项目结构

```
e:\Kaelo\
├── agent_screen/       # 屏幕捕获和元素识别模块
│   ├── screen_capture.py
│   └── element_detector.py
├── agent_comm/         # AI 通信模块
│   └── communicator.py
├── agent_exec/         # 执行模块
│   ├── command_parser.py
│   ├── safety_checker.py
│   └── action_executor.py
├── common/             # 通用模块
│   ├── data_structures.py
│   └── config.py
├── tests/              # 测试脚本
│   ├── test_windows.py
│   ├── test_screen_capture.py
│   ├── test_command_parser.py
│   └── test_safety.py
├── main.py             # 主程序入口
├── pyproject.toml      # 项目配置（用于 pip 安装）
├── requirements.txt    # 依赖列表
├── .env.example        # 配置文件模板
├── .gitignore
├── README.md
└── QUICKSTART.md       # 本文档
```

---

## 🎉 开始使用吧！

现在你已经可以：
```bash
# 测试命令
kaelo --help

# 运行你的第一个自动化任务！
kaelo "打开计算器"
```

享受智能自动化的乐趣！🚀
