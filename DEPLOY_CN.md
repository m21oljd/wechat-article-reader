# 国内云服务器部署指南（阿里云/腾讯云）

## 方案对比

| 服务商 | 轻量应用服务器价格 | 适合人群 |
|--------|-------------------|----------|
| **阿里云** | 约 60-100元/年（新用户） | 需要稳定长期运行 |
| **腾讯云** | 约 50-90元/年（新用户） | 需要稳定长期运行 |

新用户通常有首年优惠，价格很划算。

---

## 方案一：阿里云轻量应用服务器

### 1. 购买服务器

1. 访问阿里云：https://www.aliyun.com/
2. 搜索"轻量应用服务器"
3. 选择配置：
   - **地域**：选择离你最近的（如华南选深圳，华东选上海）
   - **镜像**：Ubuntu 22.04 LTS
   - **套餐**：2核2G 或更高（新用户首年约 60-100元）
4. 完成购买

### 2. 连接服务器

购买完成后，在控制台获取：
- 公网 IP 地址
- 用户名（默认 root）
- 密码（或 SSH 密钥）

使用 SSH 工具连接（如 PuTTY、XShell、或命令行）：

```bash
ssh root@你的服务器IP
```

### 3. 安装环境

连接服务器后，依次执行以下命令：

```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Python 和 pip
apt install python3 python3-pip python3-venv -y

# 安装 git
apt install git -y

# 安装 Nginx（作为反向代理）
apt install nginx -y

# 创建项目目录
mkdir -p /var/www
```

### 4. 上传代码

**方法一：使用 Git（推荐）**

```bash
cd /var/www

# 克隆你的 GitHub 仓库
git clone https://github.com/你的用户名/仓库名.git wechat-article-reader

cd wechat-article-reader
```

**方法二：使用 SCP 上传**

在本地电脑执行：

```bash
# 压缩项目文件
cd wechat-article-reader
zip -r ../wechat-article-reader.zip . -x "venv/*" "__pycache__/*" "*.pyc"

# 上传到服务器
scp ../wechat-article-reader.zip root@你的服务器IP:/var/www/

# 连接服务器解压
ssh root@你的服务器IP
cd /var/www
unzip wechat-article-reader.zip -d wechat-article-reader
```

### 5. 配置项目

```bash
cd /var/www/wechat-article-reader

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建环境变量文件
nano .env
```

在 `.env` 文件中输入：

```
DEEPSEEK_API_KEY=sk-6f0efff67cb44807a5f774a158dc119f
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

保存退出（Ctrl+O，回车，Ctrl+X）。

### 6. 使用 Gunicorn 运行

```bash
# 测试运行
gunicorn -w 4 -b 127.0.0.1:8000 app:app

# 如果正常，按 Ctrl+C 停止，配置系统服务
```

### 7. 配置系统服务（自动启动）

```bash
# 创建服务文件
nano /etc/systemd/system/wechat-reader.service
```

输入以下内容：

```ini
[Unit]
Description=WeChat Article Reader
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/wechat-article-reader
Environment="PATH=/var/www/wechat-article-reader/venv/bin"
ExecStart=/var/www/wechat-article-reader/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

保存退出，然后启动服务：

```bash
# 重新加载系统服务
systemctl daemon-reload

# 启动服务
systemctl start wechat-reader

# 设置开机自启
systemctl enable wechat-reader

# 查看状态
systemctl status wechat-reader
```

### 8. 配置 Nginx 反向代理

```bash
# 创建 Nginx 配置文件
nano /etc/nginx/sites-available/wechat-reader
```

输入以下内容：

```nginx
server {
    listen 80;
    server_name _;  # 允许任何域名或IP访问

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/wechat-article-reader/static;
        expires 30d;
    }
}
```

保存退出，然后启用配置：

```bash
# 创建软链接
ln -s /etc/nginx/sites-available/wechat-reader /etc/nginx/sites-enabled/

# 删除默认配置（可选）
rm /etc/nginx/sites-enabled/default

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

### 9. 配置防火墙

```bash
# 开放 80 端口
ufw allow 80/tcp

# 开放 443 端口（后续配置 HTTPS 用）
ufw allow 443/tcp

# 启用防火墙
ufw enable
```

### 10. 访问应用

现在可以通过服务器的公网 IP 访问了：

```
http://你的服务器IP
```

---

## 方案二：腾讯云轻量应用服务器

腾讯云的部署步骤与阿里云几乎相同，主要区别：

### 1. 购买服务器

1. 访问腾讯云：https://cloud.tencent.com/
2. 搜索"轻量应用服务器"
3. 选择配置（与阿里云类似）
4. 选择镜像：Ubuntu 22.04 LTS

### 2. 连接服务器

腾讯云提供在线 SSH 终端，也可以：

```bash
ssh ubuntu@你的服务器IP  # 腾讯云默认用户名可能是 ubuntu
```

### 3. 其余步骤

参考阿里云的步骤 3-10，完全相同。

---

## 配置 HTTPS（可选但推荐）

使用 Let's Encrypt 免费证书：

```bash
# 安装 Certbot
apt install certbot python3-certbot-nginx -y

# 获取证书
certbot --nginx -d 你的域名.com

# 如果没有域名，使用 IP 证书（自签名，浏览器会提示不安全）
```

有域名的话，先在域名服务商添加 A 记录指向服务器 IP，然后再申请证书。

---

## 日常维护命令

```bash
# 查看应用日志
journalctl -u wechat-reader -f

# 重启应用
systemctl restart wechat-reader

# 停止应用
systemctl stop wechat-reader

# 查看 Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# 更新代码后重启
cd /var/www/wechat-article-reader
git pull
systemctl restart wechat-reader
```

---

## 故障排除

### 应用无法启动

```bash
# 检查日志
journalctl -u wechat-reader -n 50

# 检查端口占用
netstat -tlnp | grep 8000
```

### Nginx 502 错误

```bash
# 检查 Gunicorn 是否运行
systemctl status wechat-reader

# 检查端口
curl http://127.0.0.1:8000
```

### 防火墙问题

```bash
# 检查防火墙状态
ufw status

# 临时关闭防火墙测试
ufw disable
```

---

## 费用估算

| 项目 | 阿里云 | 腾讯云 |
|------|--------|--------|
| 轻量服务器（首年） | 60-100元 | 50-90元 |
| 域名（可选） | 30-60元/年 | 30-60元/年 |
| **总计（首年）** | **约 90-160元** | **约 80-150元** |

续费价格会高一些，建议新用户一次性买多年，或到期后重新注册新用户购买。

---

## 优势

相比 Railway/Render：
- ✅ 国内访问速度快
- ✅ 数据在国内，合规
- ✅ 可以自己控制服务器
- ✅ 支持绑定域名和 HTTPS
- ✅ 可以运行其他服务

缺点：
- ❌ 需要一定技术基础
- ❌ 需要维护服务器
- ❌ 有费用（虽然很低）
