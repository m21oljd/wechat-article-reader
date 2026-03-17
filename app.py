"""
微信公众号文章阅读助手 - Flask后端
"""
from flask import Flask, render_template, request, jsonify
from article_parser import parse_article
from ai_analyzer import analyze_article, get_default_prompt_template, analyzer
from template_manager import get_all_templates, get_template_content, save_template, delete_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/parse', methods=['POST'])
def api_parse_article():
    """解析文章API"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({
            'success': False,
            'error': '请输入文章链接'
        })
    
    # 验证URL格式
    if not url.startswith(('http://', 'https://')):
        return jsonify({
            'success': False,
            'error': '请输入有效的URL链接'
        })
    
    # 解析文章
    result = parse_article(url)
    return jsonify(result)


@app.route('/api/analyze', methods=['POST'])
def api_analyze_article():
    """分析文章API"""
    data = request.get_json()
    content = data.get('content', '').strip()
    custom_prompt = data.get('custom_prompt', '').strip()
    
    if not content:
        return jsonify({
            'success': False,
            'error': '文章内容为空'
        })
    
    # 限制内容长度（避免超出token限制）
    max_length = 15000
    if len(content) > max_length:
        content = content[:max_length] + '\n\n[文章内容过长，已截断...]'
    
    # 使用自定义提示词或默认提示词
    prompt = custom_prompt if custom_prompt else None
    result = analyze_article(content, prompt)
    
    return jsonify(result)


@app.route('/api/prompt-template', methods=['GET'])
def api_get_prompt_template():
    """获取默认提示词模板"""
    return jsonify({
        'success': True,
        'data': {
            'template': get_default_prompt_template()
        }
    })


@app.route('/api/check-config', methods=['GET'])
def api_check_config():
    """检查API配置状态"""
    return jsonify({
        'success': True,
        'data': {
            'ai_configured': analyzer.is_configured()
        }
    })


# ==================== 模板管理 API ====================

@app.route('/api/templates', methods=['GET'])
def api_get_templates():
    """获取所有模板列表"""
    templates = get_all_templates()
    return jsonify({
        'success': True,
        'data': {
            'templates': templates
        }
    })


@app.route('/api/templates/<template_id>', methods=['GET'])
def api_get_template_content(template_id):
    """获取指定模板的完整内容"""
    content = get_template_content(template_id)
    if content:
        return jsonify({
            'success': True,
            'data': {
                'content': content
            }
        })
    return jsonify({
        'success': False,
        'error': '模板不存在'
    })


@app.route('/api/templates', methods=['POST'])
def api_save_template():
    """保存新模板"""
    data = request.get_json()
    name = data.get('name', '').strip()
    content = data.get('content', '').strip()
    description = data.get('description', '').strip()
    
    if not name:
        return jsonify({
            'success': False,
            'error': '模板名称不能为空'
        })
    
    if not content:
        return jsonify({
            'success': False,
            'error': '模板内容不能为空'
        })
    
    # 确保模板包含必要的占位符
    if '{article_content}' not in content:
        return jsonify({
            'success': False,
            'error': '模板内容必须包含 {article_content} 占位符'
        })
    
    result = save_template(name, content, description)
    return jsonify({
        'success': True,
        'data': result
    })


@app.route('/api/templates/<template_id>', methods=['DELETE'])
def api_delete_template(template_id):
    """删除用户模板"""
    success = delete_template(template_id)
    if success:
        return jsonify({
            'success': True,
            'message': '模板已删除'
        })
    return jsonify({
        'success': False,
        'error': '无法删除内置模板或模板不存在'
    })


# 确保模板目录存在
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
