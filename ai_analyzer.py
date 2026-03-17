"""
AI文章分析模块
"""
import os
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, READING_ASSISTANT_PROMPT


class AIAnalyzer:
    """AI文章分析器"""
    
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.base_url = OPENAI_BASE_URL
        self.model = OPENAI_MODEL
        self.client = None
        
        if self.api_key:
            try:
                import httpx
                # 创建自定义 http_client 以避免 proxies 参数问题
                http_client = httpx.Client()
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    http_client=http_client
                )
            except Exception:
                # 如果失败，尝试不使用 http_client
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
    
    def is_configured(self) -> bool:
        """检查是否已配置API密钥"""
        return bool(self.api_key and self.client)
    
    def analyze_article(self, article_content: str, custom_prompt: str = None) -> dict:
        """
        使用AI分析文章
        
        Args:
            article_content: 文章内容
            custom_prompt: 自定义提示词（可选）
            
        Returns:
            dict: 包含分析结果的字典
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': '未配置OpenAI API密钥，请在 .env 文件中设置 OPENAI_API_KEY'
            }
        
        try:
            # 准备提示词
            if custom_prompt:
                prompt = custom_prompt.format(article_content=article_content)
            else:
                prompt = READING_ASSISTANT_PROMPT.format(article_content=article_content)
            
            # 调用AI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': '你是一位专业的阅读助手，擅长深度分析文章并提炼核心内容。请用中文回答。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # 提取分析结果
            analysis = response.choices[0].message.content
            
            return {
                'success': True,
                'data': {
                    'analysis': analysis,
                    'model': self.model,
                    'tokens_used': response.usage.total_tokens if response.usage else None
                }
            }
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"AI分析错误详情: {error_detail}")
            return {
                'success': False,
                'error': f'AI分析出错: {str(e)}',
                'detail': error_detail
            }
    
    def analyze_with_custom_prompt(self, article_content: str, prompt_template: str) -> dict:
        """
        使用自定义提示词分析文章
        
        Args:
            article_content: 文章内容
            prompt_template: 提示词模板，需要包含 {article_content} 占位符
            
        Returns:
            dict: 包含分析结果的字典
        """
        return self.analyze_article(article_content, prompt_template)


# 全局分析器实例
analyzer = AIAnalyzer()


def analyze_article(article_content: str, custom_prompt: str = None) -> dict:
    """便捷函数：分析文章"""
    return analyzer.analyze_article(article_content, custom_prompt)


def get_default_prompt_template() -> str:
    """获取默认提示词模板"""
    return READING_ASSISTANT_PROMPT
