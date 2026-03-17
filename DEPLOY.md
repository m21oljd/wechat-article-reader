# 部署指南

## 方案一：部署到 Railway（推荐，有免费额度）

### 1. 准备工作

- 注册 Railway 账号：https://railway.app/
- 安装 Git（如果还没有）

### 2. 上传代码到 GitHub

```bash
# 在项目目录下初始化 git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 在 GitHub 创建新仓库，然后关联并推送
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 3. 在 Railway 部署

1. 登录 Railway，点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你的仓库
4. 点击 "Deploy"

### 4. 配置环境变量

在 Railway 的 Variables 页面添加：

```
DEEPSEEK_API_KEY=sk-你的API密钥
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

### 5. 完成

Railway 会自动分配一个域名，点击即可访问！

---

## 方案二：部署到 Render（免费）

### 1. 准备工作

- 注册 Render 账号：https://render.com/
- 代码已上传到 GitHub

### 2. 创建 Web Service

1. 登录 Render，点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库
3. 填写配置：
   - **Name**: wechat-article-reader
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 3. 配置环境变量

在 Environment 页面添加：

```
DEEPSEEK_API_KEY=sk-你的API密钥
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

### 4. 部署

点击 "Create Web Service"，等待部署完成。

---

## 方案三：部署到 Vercel（需要适配）

Vercel 主要支持 Serverless 函数，对 Flask 支持有限，建议使用 Railway 或 Render。

---

## 注意事项

### API 密钥安全

- **永远不要**将 `.env` 文件提交到 GitHub
- 已在 `.gitignore` 中排除了 `.env` 文件
- 只在云平台的 Environment Variables 中设置密钥

### 免费额度

| 平台 | 免费额度 | 限制 |
|------|---------|------|
| Railway | $5/月 | 每月500小时运行时间 |
| Render | 免费 | 15分钟无访问会休眠 |

### 自定义域名（可选）

两个平台都支持绑定自定义域名，在设置页面配置即可。

---

## 部署后使用

部署完成后，你会得到一个类似 `https://wechat-article-reader.railway.app` 的网址：

1. 在手机上浏览器打开这个网址
2. 粘贴微信公众号文章链接
3. 选择模板，点击分析
4. 随时随地使用！

---

## 故障排除

### 部署失败

1. 检查 `requirements.txt` 是否包含所有依赖
2. 检查 `Procfile` 是否正确
3. 查看平台提供的日志

### API 调用失败

1. 检查环境变量是否正确设置
2. 确认 DeepSeek API Key 有效且有余额
3. 查看应用日志排查错误

### 模板不显示

用户保存的模板存储在本地文件 `user_templates.json`，部署到云端后：
- 内置模板仍然可用
- 用户模板需要重新保存（或使用数据库存储，需要额外开发）
