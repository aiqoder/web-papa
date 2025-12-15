# Web Crawler API

一个基于FastAPI和Playwright的Web爬虫API服务，用于将网页内容解析为Markdown格式。

## 功能特性

- 🔄 异步网页爬取，支持多种网站
- 📝 智能HTML到Markdown转换
- 🔗 支持提取网页中的所有链接
- 🎯 网站特定解析规则支持
- 📱 响应式设计，支持各种设备
- 🚀 高性能，基于FastAPI框架

## 技术栈

- Python 3.11+
- FastAPI - Web框架
- Uvicorn - ASGI服务器
- Playwright - 网页爬虫
- BeautifulSoup4 - HTML解析
- PyYAML - 配置管理
- markdownify - HTML到Markdown转换

## 项目结构

```
.
├── app/                 # 主应用目录
│   ├── api.py           # API接口定义
│   ├── crawler.py       # 网页爬虫实现
│   ├── parser.py        # 网页解析器
│   ├── markdown.py      # Markdown转换器
│   ├── config.py        # 配置管理器
│   └── main.py          # 应用入口
├── configs/             # 网站解析规则配置
│   ├── default.yaml     # 默认配置
│   ├── wechat.yaml      # 微信公众号配置
│   ├── zhihu.yaml       # 知乎配置
│   └── ...              # 其他网站配置
├── docker/              # Docker相关配置
├── requirements.txt     # 项目依赖
├── pyproject.toml       # 项目配置
└── README.md            # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install
```

### 2. 运行服务

```bash
# 使用uvicorn直接运行
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 或使用Python脚本运行
python -m app.main
```

### 3. 访问API文档

服务启动后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API调用

### 1. 解析网页为Markdown

**端点**: `POST /parse`

**请求体**:
```json
{
  "url": "https://example.com/article",
  "config_name": "default"  // 可选，指定配置名称
}
```

**响应**:
```json
{
  "success": true,
  "title": "文章标题",
  "content": "Markdown格式的文章内容",
  "url": "https://example.com/article",
  "links": [
    {
      "url": "https://example.com/link1",
      "title": "链接1标题"
    }
  ],
  "error": null
}
```

### 2. 提取网页链接

**端点**: `POST /extract-links`

**请求体**:
```json
{
  "url": "https://example.com/article"
}
```

**响应**:
```json
{
  "success": true,
  "title": "网页标题",
  "links": [
    {
      "url": "https://example.com/link1",
      "title": "链接1标题"
    }
  ],
  "url": "https://example.com/article",
  "error": null
}
```

### 3. 健康检查

**端点**: `GET /`

**响应**:
```json
{
  "status": "ok",
  "message": "Web Crawler API is running",
  "docs": "/docs"
}
```

## 网站规则集成方式

### 1. 配置文件结构

在`configs/`目录下创建YAML配置文件，例如`example.yaml`，包含以下内容：

```yaml
title_selector: "title"          # 标题选择器
content_selector: ".article-content"  # 内容选择器
exclude_selectors:               # 排除的选择器
  - "script"
  - "style"
  - ".advertisement"
  - "nav"
  - "footer"
```

### 2. 配置参数说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `title_selector` | string | CSS选择器，用于提取网页标题 |
| `content_selector` | string | CSS选择器，用于提取网页主要内容 |
| `exclude_selectors` | array | CSS选择器数组，用于排除不需要的元素 |

### 3. 配置匹配规则

1. **显式指定**：通过API请求中的`config_name`参数指定配置名称
2. **域名自动匹配**：根据URL的域名自动匹配配置文件
   - 例如：`www.zhihu.com`会自动匹配`configs/zhihu.yaml`
3. **默认配置**：如果没有匹配到特定配置，会使用`configs/default.yaml`

### 4. 添加新网站规则

1. 在`configs/`目录下创建新的YAML配置文件，例如`newsite.yaml`
2. 根据网站结构编写选择器规则
3. 更新`app/config.py`中的域名映射（可选，用于自动匹配）

## 可用配置

目前支持的网站配置包括：

- `default` - 默认配置，适用于大多数网站
- `52pojie` - 吾爱破解论坛配置

- `bilibili` - Bilibili配置
- `coursera` - Coursera配置
- `csdn` - CSDN配置
- `douyin` - 抖音配置
- `eastmoney` - 东方财富配置
- `gamersky` - 游民星空配置
- `github` - GitHub配置
- `hupu` - 虎扑配置
- `icourse163` - 中国大学MOOC配置
- `iqiyi` - 爱奇艺配置
- `jd` - 京东配置
- `juejin` - 掘金配置
- `medium` - Medium配置
- `meituan` - 美团配置
- `open.163` - 网易开放平台配置
- `people` - 人民网配置
- `right.com.cn` - 恩山无线论坛配置
- `sinafinance` - 新浪财经配置
- `sports.qq.com` - 腾讯体育配置
- `sports.sina.com.cn` - 新浪体育配置
- `stackoverflow` - Stack Overflow配置
- `steam` - Steam配置
- `taobao` - 淘宝配置
- `taptap` - TapTap配置
- `thepaper` - 澎湃新闻配置
- `v.qq.com` - 腾讯视频配置
- `wechat` - 微信公众号配置
- `weibo` - 微博配置
- `xinhuanet` - 新华网配置
- `xueqiu` - 雪球配置
- `youtube` - YouTube配置
- `zhihu` - 知乎配置

## Docker部署

### 1. 构建Docker镜像

```bash
docker build -t web-crawler-api -f docker/Dockerfile .
```

### 2. 运行Docker容器

```bash
docker run -d -p 8000:8000 web-crawler-api
```

### 3. 使用Docker Compose

```bash
docker-compose up -d
```

## 开发指南

### 1. 环境设置

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 代码风格

项目使用PEP 8代码风格，建议使用以下工具进行代码检查：

```bash
# 安装代码检查工具
pip install flake8 black

# 检查代码
flake8 app/

# 自动格式化代码
black app/
```

### 3. 测试

```bash
# 运行测试脚本
python test_wechat.py
```

## 常见问题

### 1. 爬取不到网页内容

- 检查URL是否正确
- 检查网站是否有反爬机制
- 尝试调整爬虫的等待时间和加载策略

### 2. 解析结果不准确

- 检查配置文件中的选择器是否正确
- 查看网页HTML结构，调整选择器规则
- 尝试添加更多排除选择器

### 3. 服务启动失败

- 检查端口是否被占用
- 确保所有依赖已正确安装
- 查看日志输出，定位错误原因
