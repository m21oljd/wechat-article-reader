# 微信公众号文章阅读助手

一个基于 Flask 的网页应用，可以自动抓取微信公众号文章内容，并使用 AI 进行深度分析。

## 功能特点

- 🔗 **文章解析**：粘贴微信公众号文章链接，自动提取标题、作者、正文等内容
- 🤖 **AI 分析**：使用 OpenAI API 对文章进行深度分析
- 📝 **自定义提示词**：支持使用你自己的分析框架和提示词
- 📋 **一键复制**：分析结果支持一键复制
- 📱 **响应式设计**：支持桌面和移动设备

## 安装步骤

1. **克隆或下载项目**
   ```bash
   cd wechat-article-reader
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 API 密钥**
   
   复制 `.env.example` 文件为 `.env`，并填入你的 OpenAI API 密钥：
   ```bash
   cp .env.example .env
   ```
   
   编辑 `.env` 文件：
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL=gpt-4o-mini
   ```

4. **运行应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   
   打开浏览器访问 http://localhost:5000

## 使用方法

1. 在微信中打开你想分析的文章
2. 点击右上角「...」→「复制链接」
3. 将链接粘贴到网页的输入框中
4. 点击「解析文章」按钮
5. （可选）在自定义提示词框中输入你自己的分析框架
6. 点击「AI分析」按钮，等待分析结果

## 项目结构

```
wechat-article-reader/
├── app.py                 # Flask 主应用
├── article_parser.py      # 文章解析模块
├── ai_analyzer.py         # AI 分析模块
├── config.py             # 配置文件
├── requirements.txt      # Python 依赖
├── .env.example         # 环境变量示例
├── templates/
│   └── index.html       # 前端页面
└── static/
    └── css/
        └── style.css    # 样式文件
```

## 自定义提示词

你可以在 `config.py` 中修改默认的阅读助手提示词模板，或者在网页上直接输入自定义提示词。

提示词模板需要包含 `{article_content}` 占位符，用于插入文章内容。

## 注意事项

1. 需要有效的 OpenAI API 密钥才能使用 AI 分析功能
2. 文章内容过长时会自动截断（约15000字符），以避免超出 API 的 token 限制
3. 由于微信公众号的反爬机制，部分文章可能无法正常解析
4. 建议使用自己的 API 密钥，避免频繁调用导致额度不足

## 技术栈

- **后端**: Python + Flask
- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **文章解析**: BeautifulSoup4 + html2text
- **AI 分析**: OpenAI API

## License

MIT License
