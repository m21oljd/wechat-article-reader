"""
微信公众号文章解析模块
"""
import re
import requests
from bs4 import BeautifulSoup
import html2text


class ArticleParser:
    """文章解析器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.ignore_tables = False
        self.html_converter.body_width = 0
    
    def parse_url(self, url: str) -> dict:
        """
        解析文章URL，提取标题、作者、内容等信息
        
        Args:
            url: 文章链接
            
        Returns:
            dict: 包含文章信息的字典
        """
        try:
            # 发送请求获取页面
            response = requests.get(url, headers=self.headers, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'请求失败，状态码: {response.status_code}'
                }
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 提取文章信息
            article_info = self._extract_article_info(soup, url)
            
            return {
                'success': True,
                'data': article_info
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'网络请求错误: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'解析错误: {str(e)}'
            }
    
    def _extract_article_info(self, soup: BeautifulSoup, url: str) -> dict:
        """提取文章详细信息"""
        
        # 提取标题
        title = self._extract_title(soup)
        
        # 提取作者
        author = self._extract_author(soup)
        
        # 提取发布时间
        publish_time = self._extract_publish_time(soup)
        
        # 提取公众号名称
        account_name = self._extract_account_name(soup)
        
        # 提取正文内容
        content_html, content_text = self._extract_content(soup)
        
        # 提取封面图
        cover_image = self._extract_cover_image(soup)
        
        return {
            'title': title,
            'author': author,
            'account_name': account_name,
            'publish_time': publish_time,
            'url': url,
            'content_html': content_html,
            'content_text': content_text,
            'cover_image': cover_image,
            'word_count': len(content_text)
        }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取文章标题"""
        # 尝试多种方式提取标题
        selectors = [
            'h1.rich_media_title',
            'h2.rich_media_title',
            '#activity_name',
            'h1.title',
            'h2.title',
            'meta[property="og:title"]',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if selector.startswith('meta'):
                    return element.get('content', '').strip()
                else:
                    return element.get_text(strip=True)
        
        return '未知标题'
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """提取作者"""
        selectors = [
            '#js_name',
            '.profile_nickname',
            'a#js_name',
            'span.profile_nickname',
            'meta[name="author"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if selector.startswith('meta'):
                    return element.get('content', '').strip()
                else:
                    return element.get_text(strip=True)
        
        return '未知作者'
    
    def _extract_account_name(self, soup: BeautifulSoup) -> str:
        """提取公众号名称"""
        selectors = [
            '#js_name',
            '.profile_nickname',
            'a#js_name'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        return '未知公众号'
    
    def _extract_publish_time(self, soup: BeautifulSoup) -> str:
        """提取发布时间"""
        selectors = [
            '#publish_time',
            '.rich_media_meta_text',
            'em#publish_time',
            '#js_publish_time'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # 尝试从脚本中提取
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                time_match = re.search(r'var\s+publish_time\s*=\s*["\']([^"\']+)["\']', script.string)
                if time_match:
                    return time_match.group(1)
        
        return ''
    
    def _extract_content(self, soup: BeautifulSoup) -> tuple:
        """提取正文内容"""
        content_selectors = [
            '#js_content',
            '.rich_media_content',
            '#js_article_content',
            '.article-content',
            'article'
        ]
        
        content_html = ''
        content_text = ''
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                # 清理内容
                self._clean_content(element)
                content_html = str(element)
                content_text = self.html_converter.handle(content_html)
                # 清理文本
                content_text = self._clean_text(content_text)
                break
        
        return content_html, content_text
    
    def _clean_content(self, element):
        """清理内容中的无关元素"""
        # 移除脚本和样式
        for tag in element.find_all(['script', 'style', 'iframe']):
            tag.decompose()
        
        # 移除广告相关
        for tag in element.find_all(class_=re.compile(r'ad|qr|reward|vote')):
            tag.decompose()
        
        # 移除空标签
        for tag in element.find_all():
            if len(tag.get_text(strip=True)) == 0 and tag.name not in ['br', 'img']:
                tag.decompose()
    
    def _clean_text(self, text: str) -> str:
        """清理文本内容"""
        # 移除多余的空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        # 移除行首行尾空白
        text = '\n'.join(line.strip() for line in text.split('\n'))
        # 移除特殊字符
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', text)
        return text.strip()
    
    def _extract_cover_image(self, soup: BeautifulSoup) -> str:
        """提取封面图片"""
        # 尝试从meta标签获取
        meta_selectors = [
            'meta[property="og:image"]',
            'meta[property="twitter:image"]'
        ]
        
        for selector in meta_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get('content', '')
        
        # 尝试从内容中获取第一张图片
        content = soup.select_one('#js_content')
        if content:
            first_img = content.find('img')
            if first_img:
                return first_img.get('data-src', first_img.get('src', ''))
        
        return ''


# 全局解析器实例
parser = ArticleParser()


def parse_article(url: str) -> dict:
    """便捷函数：解析文章"""
    return parser.parse_url(url)
