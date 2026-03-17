"""
模板管理模块
支持保存、加载、删除用户自定义模板
"""
import json
import os
from typing import List, Dict, Optional

# 模板存储文件路径
TEMPLATES_FILE = 'user_templates.json'

# 内置默认模板
DEFAULT_TEMPLATES = [
    {
        "id": "default_general",
        "name": "📊 通用分析模板",
        "description": "适用于各类文章的通用分析框架，提取核心观点、金句和新概念",
        "content": """你是一个公众号文章分析助手。你的任务是快速提炼文章的核心价值，帮助用户决定是否值得深读。

## 输出要求
请按以下结构输出分析结果，使用Markdown格式：

### 📝 文章摘要
用100字左右概括文章主旨，包含文章主题 + 核心结论 + 独特价值。

### 💡 核心观点
列出文章的2-5个核心观点，每个观点包含：
- **观点**：一句话概括（不超过30字，必须是完整判断句）
- **论据**：支撑该观点的具体论据、案例或数据（50-100字）

### ✨ 金句摘录
摘录1-5句原文中最有洞察力或表达力的句子。必须是原文原话。

### 🔮 新概念
识别文章中的新兴词汇或概念（如AI Agent、具身智能等），每个概念包含：
- **术语**：新概念名称
- **解释**：简要解释含义（20-50字）

### 📊 文章评价
- **文章类型**：深度分析/观点文/资讯/教程/软文
- **质量评价**：高/中/低，简要说明原因
- **阅读建议**：是否值得深读，适合什么人群

## 分析原则

1. **观点提炼**
   - 每个观点必须是完整的判断句，不是模糊描述
   - 好的观点示例："AI 不会取代人类，但会取代不会用 AI 的人"
   - 差的观点示例："关于 AI 的一些思考"

2. **论据提取**
   - 如果原文只有观点没有论据，注明"原文未提供具体论据"

3. **金句筛选**
   - 优先选择：有洞察力的判断、生动的比喻、反直觉的表述

4. **特殊情况处理**
   - 如果文章质量低/内容空洞，如实说明
   - 如果是软文/广告，明确标注

---

**原文内容**：
{article_content}""",
        "is_builtin": True
    },
    {
        "id": "default_social",
        "name": "📚 社科人文模板",
        "description": "专注于社会人文类文章的深度解读，分析叙事内核、人物价值与社会意义",
        "content": """你是一个专注于社会人文类文章的分析助手。你的任务是深入解读文章的叙事内核、人物价值与社会意义。

## 输出要求
请按以下结构输出分析结果，使用Markdown格式：

### 📖 叙事摘要
用150字左右复述核心故事，突出主角、核心冲突与结局，像故事梗概一样有起承转合。

### 👤 人物分析
- **主角画像**：关键身份标签与背景（如：90后海归硕士、前金融从业者）
- **核心动机**：驱动主角行动或转变的内在动机
- **转变弧光**：主角经历的关键转变或成长

### 🌍 社会议题
列出文章揭示的1-3个社会议题，每个包含：
- **议题**：核心社会议题名称
- **具体展现**：该议题在文中的案例、细节或矛盾
- **引发思考**：文章向读者抛出的潜在问题

### 💭 情感共鸣
- **感人细节**：文中最具感染力的1-3个细节或瞬间（描述性引用）
- **情感基调**：文章试图唤起的主要情感（如共情、反思、温暖、无力感）

### ✨ 金句摘录
摘录1-3句最具代表性的原文金句，优先选择体现人物心声、文章主旨的句子。

### 🎭 叙事手法
简要分析文章采用的叙事手法（如：第一人称自述、案例穿插、今昔对比、倒叙等）。

## 分析原则

1. **叙事优先**：将文章视为一个"故事"来解读
2. **人物深度**：挖掘人物表象下的动机与弧光，而非罗列简历
3. **议题关联**：从具体故事提炼普遍性社会问题
4. **情感捕捉**：关注"于无声处听惊雷"的细节
5. **紧扣文本**：所有分析都应源自文中具体描述

---

**原文内容**：
{article_content}""",
        "is_builtin": True
    }
]


class TemplateManager:
    """模板管理器"""
    
    def __init__(self):
        self.templates_file = TEMPLATES_FILE
        self.user_templates = self._load_user_templates()
    
    def _load_user_templates(self) -> List[Dict]:
        """从文件加载用户保存的模板"""
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_user_templates(self):
        """保存用户模板到文件"""
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_templates, f, ensure_ascii=False, indent=2)
    
    def get_all_templates(self) -> List[Dict]:
        """获取所有模板（内置 + 用户自定义）"""
        all_templates = []
        
        # 添加内置模板
        for template in DEFAULT_TEMPLATES:
            all_templates.append({
                "id": template["id"],
                "name": template["name"],
                "description": template["description"],
                "is_builtin": True
            })
        
        # 添加用户模板
        for template in self.user_templates:
            all_templates.append({
                "id": template["id"],
                "name": template["name"],
                "description": template.get("description", ""),
                "is_builtin": False
            })
        
        return all_templates
    
    def get_template_content(self, template_id: str) -> Optional[str]:
        """获取指定模板的完整内容"""
        # 先查找内置模板
        for template in DEFAULT_TEMPLATES:
            if template["id"] == template_id:
                return template["content"]
        
        # 再查找用户模板
        for template in self.user_templates:
            if template["id"] == template_id:
                return template["content"]
        
        return None
    
    def save_template(self, name: str, content: str, description: str = "") -> Dict:
        """保存新模板"""
        import uuid
        
        # 生成唯一ID
        template_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # 创建模板对象
        new_template = {
            "id": template_id,
            "name": name,
            "description": description,
            "content": content,
            "created_at": self._get_timestamp()
        }
        
        # 添加到用户模板列表
        self.user_templates.append(new_template)
        self._save_user_templates()
        
        return {
            "id": template_id,
            "name": name,
            "description": description,
            "is_builtin": False
        }
    
    def delete_template(self, template_id: str) -> bool:
        """删除用户模板（内置模板不能删除）"""
        # 检查是否为内置模板
        for template in DEFAULT_TEMPLATES:
            if template["id"] == template_id:
                return False
        
        # 查找并删除用户模板
        for i, template in enumerate(self.user_templates):
            if template["id"] == template_id:
                del self.user_templates[i]
                self._save_user_templates()
                return True
        
        return False
    
    def update_template(self, template_id: str, name: str = None, 
                       content: str = None, description: str = None) -> bool:
        """更新用户模板"""
        for template in self.user_templates:
            if template["id"] == template_id:
                if name:
                    template["name"] = name
                if content:
                    template["content"] = content
                if description is not None:
                    template["description"] = description
                template["updated_at"] = self._get_timestamp()
                self._save_user_templates()
                return True
        return False
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


# 全局模板管理器实例
template_manager = TemplateManager()


# 便捷函数
def get_all_templates() -> List[Dict]:
    """获取所有模板"""
    return template_manager.get_all_templates()


def get_template_content(template_id: str) -> Optional[str]:
    """获取模板内容"""
    return template_manager.get_template_content(template_id)


def save_template(name: str, content: str, description: str = "") -> Dict:
    """保存模板"""
    return template_manager.save_template(name, content, description)


def delete_template(template_id: str) -> bool:
    """删除模板"""
    return template_manager.delete_template(template_id)
