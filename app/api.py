from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any, List
import logging

from .crawler import WebCrawler
from .parser import web_parser
from .markdown import markdown_converter
from .config import config_manager

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Web Crawler API",
    description="A web crawler API that converts web pages to Markdown using Playwright",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 链接项模型
class LinkItem(BaseModel):
    url: str
    title: str

# 请求模型
class ParseRequest(BaseModel):
    url: HttpUrl
    config_name: Optional[str] = None
    """
    解析配置名称，用于指定不同网站的解析规则
    
    可用的配置名称：
    - default: 默认配置，适用于大多数网站
    - 52pojie: 吾爱破解论坛配置
    - bilibili: Bilibili配置
    - csdn: CSDN配置
    - juejin: 掘金配置
    - right.com.cn: 恩山无线论坛配置
    - sinafinance: 新浪财经配置
    - wechat: 微信公众号配置
    - zhihu: 知乎配置
    """

# 响应模型
class ParseResponse(BaseModel):
    success: bool
    title: str
    content: str
    url: str
    links: List[LinkItem]
    error: Optional[str] = None

# 链接提取请求模型
class ExtractLinksRequest(BaseModel):
    url: HttpUrl

# 链接提取响应模型
class ExtractLinksResponse(BaseModel):
    success: bool
    title: str
    links: List[LinkItem]
    url: str
    error: Optional[str] = None

@app.post("/parse", response_model=ParseResponse, summary="Parse web page to Markdown")
async def parse_web_page(request: ParseRequest):
    """
    解析网页并转换为Markdown格式
    
    Args:
        request: 请求体，包含以下字段：
            url: 目标网页的URL
            config_name: 解析配置名称，可选，用于指定不同网站的解析规则
                可用的配置名称：
                - default: 默认配置，适用于大多数网站
                - 52pojie: 吾爱破解论坛配置
                
                - bilibili: Bilibili配置
                - csdn: CSDN配置
                - juejin: 掘金配置
                - right.com.cn: 恩山无线论坛配置
                - sinafinance: 新浪财经配置
                - wechat: 微信公众号配置
                - zhihu: 知乎配置
        
    Returns:
        包含标题、Markdown内容、链接列表和状态的响应
    """
    url = str(request.url)
    config_name = request.config_name
    
    logger.info(f"Received parse request for URL: {url}, config: {config_name}")
    
    try:
        # 获取配置
        config = config_manager.get_config(config_name=config_name, url=url)
        logger.info(f"Using config: {config}")
        
        # 使用异步爬虫获取网页内容
        logger.info(f"Crawling URL: {url}")
        async with WebCrawler(headless=True) as crawler:
            # 使用更快的加载策略和更长的超时时间
            html_content = await crawler.get_page_content(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )
        
        # 解析网页内容
        logger.info("Parsing web content")
        title, content_html = web_parser.parse(html_content, config)
        
        # 转换为Markdown
        logger.info("Converting to Markdown")
        markdown_content = markdown_converter.convert(content_html, title)
        
        # 提取所有链接
        logger.info("Extracting links...")
        links = web_parser.extract_links(html_content, url)
        
        # 返回成功响应
        logger.info(f"Successfully parsed URL: {url}, extracted {len(links)} links")
        return ParseResponse(
            success=True,
            title=title,
            content=markdown_content,
            url=url,
            links=links
        )
    
    except Exception as e:
        # 记录错误
        logger.error(f"Error parsing URL {url}: {str(e)}", exc_info=True)
        
        # 返回错误响应
        return ParseResponse(
            success=False,
            title="",
            content="",
            url=url,
            links=[],
            error=str(e)
        )

@app.post("/extract-links", response_model=ExtractLinksResponse, summary="Extract all links from web page")
async def extract_links(request: ExtractLinksRequest):
    """
    提取网页中所有的URL和标题
    
    Args:
        request: 请求体，包含目标URL
        
    Returns:
        包含标题和链接列表的响应
    """
    url = str(request.url)
    
    logger.info(f"Received extract links request for URL: {url}")
    
    try:
        # 使用异步爬虫获取网页内容
        logger.info(f"Crawling URL: {url}")
        async with WebCrawler(headless=True) as crawler:
            # 使用更快的加载策略和更长的超时时间
            html_content = await crawler.get_page_content(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )
        
        # 创建BeautifulSoup对象用于提取标题
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 提取网页标题
        title = ""
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # 提取所有链接
        logger.info("Extracting links...")
        links = web_parser.extract_links(html_content, url)
        
        # 返回成功响应
        logger.info(f"Successfully extracted {len(links)} links from URL: {url}")
        return ExtractLinksResponse(
            success=True,
            title=title,
            links=links,
            url=url
        )
    
    except Exception as e:
        # 记录错误
        logger.error(f"Error extracting links from URL {url}: {str(e)}", exc_info=True)
        
        # 返回错误响应
        return ExtractLinksResponse(
            success=False,
            title="",
            links=[],
            url=url,
            error=str(e)
        )

@app.get("/", summary="Health check")
async def health_check():
    """
    健康检查接口
    
    Returns:
        健康状态信息
    """
    return {
        "status": "ok",
        "message": "Web Crawler API is running",
        "docs": "/docs"
    }
