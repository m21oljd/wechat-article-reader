# 配置文件
import os
from dotenv import load_dotenv

load_dotenv()

# API 配置（支持 OpenAI、DeepSeek 等兼容 API）
# 优先级：DEEPSEEK_API_KEY > OPENAI_API_KEY
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '') or DEEPSEEK_API_KEY

OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

# 阅读助手提示词模板
READING_ASSISTANT_PROMPT = """
你是一位专业的阅读助手，擅长深度分析文章并提炼核心内容。

请对以下文章进行全面分析，并按照以下结构输出：

## 📋 文章概览
- **标题**：
- **作者/来源**：
- **文章类型**：
- **阅读难度**：⭐（1-5星）

## 🎯 核心观点
用2-3句话概括文章的核心论点和主要结论。

## 📊 内容结构
列出文章的主要章节/段落及其核心内容：
1. 
2. 
3. 

## 💡 关键要点
提取文章中的3-5个最重要的要点：
- 
- 
- 

## 🔍 深度分析
- **论证逻辑**：分析作者的论证方式和逻辑链条
- **证据支持**：列举文章中使用的关键证据、数据或案例
- **潜在偏见**：指出可能存在的观点偏向或局限性

## 🤔 批判性思考
- **优点**：文章写得好的地方
- **不足**：文章可能存在的问题或遗漏
- **延伸思考**：这篇文章引发的进一步思考

## 📚 相关推荐
基于这篇文章的内容，推荐相关的阅读方向或话题。

## ⏱️ 阅读建议
- **适合人群**：
- **阅读时长**：
- **建议阅读方式**（精读/略读/跳读）：

---

**原文内容**：
{article_content}
"""
