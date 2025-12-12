from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from typing import Optional, Dict, Any
import asyncio

class WebCrawler:
    """
    网页爬虫引擎，使用Playwright进行网页请求和内容获取（异步版）
    """
    
    def __init__(self, headless: bool = True):
        """
        初始化爬虫引擎
        
        Args:
            headless: 是否使用无头浏览器模式，默认为True
        """
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
    
    async def __aenter__(self):
        """
        进入异步上下文管理器，初始化Playwright和浏览器
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--single-process",
                "--disable-gpu"
            ]
        )
        self.context = await self.browser.new_context()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        退出异步上下文管理器，关闭浏览器和Playwright
        """
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def get_page_content(self, url: str, wait_time: int = 5, wait_for_selector: Optional[str] = None, wait_until: str = "domcontentloaded", timeout: int = 60000) -> str:
        """
        获取网页内容
        
        Args:
            url: 目标URL
            wait_time: 页面加载等待时间（秒），默认为5秒
            wait_for_selector: 等待特定元素出现的CSS选择器，可选
            wait_until: 页面加载完成条件，默认为"domcontentloaded"
            timeout: 页面加载超时时间（毫秒），默认为60秒
            
        Returns:
            网页HTML内容
        """
        if not self.context:
            raise RuntimeError("Browser context not initialized. Use async with statement.")
        
        page: Page = await self.context.new_page()
        
        try:
            # 导航到目标URL，使用更快的加载策略和更长的超时时间
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            
            # 等待指定时间，确保页面完全加载
            await page.wait_for_timeout(wait_time * 1000)
            
            # 如果指定了选择器，等待该元素出现
            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector, timeout=10000)
            
            # 获取页面HTML内容
            content = await page.content()
            return content
        finally:
            await page.close()
    
    async def get_page_title(self, url: str, wait_time: int = 3, wait_until: str = "domcontentloaded", timeout: int = 60000) -> str:
        """
        获取网页标题
        
        Args:
            url: 目标URL
            wait_time: 页面加载等待时间（秒），默认为3秒
            wait_until: 页面加载完成条件，默认为"domcontentloaded"
            timeout: 页面加载超时时间（毫秒），默认为60秒
            
        Returns:
            网页标题
        """
        if not self.context:
            raise RuntimeError("Browser context not initialized. Use async with statement.")
        
        page: Page = await self.context.new_page()
        
        try:
            # 导航到目标URL，使用更快的加载策略和更长的超时时间
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            
            # 等待指定时间
            await page.wait_for_timeout(wait_time * 1000)
            
            # 获取页面标题
            title = await page.title()
            return title
        finally:
            await page.close()

# 便捷函数：单次爬取网页内容
async def crawl(url: str, headless: bool = True, wait_time: int = 5, wait_until: str = "domcontentloaded", timeout: int = 60000) -> str:
    """
    便捷函数，单次爬取网页内容
    
    Args:
        url: 目标URL
        headless: 是否使用无头浏览器模式
        wait_time: 页面加载等待时间（秒）
        wait_until: 页面加载完成条件，默认为"domcontentloaded"
        timeout: 页面加载超时时间（毫秒），默认为60秒
        
    Returns:
        网页HTML内容
    """
    async with WebCrawler(headless=headless) as crawler:
        return await crawler.get_page_content(url, wait_time=wait_time, wait_until=wait_until, timeout=timeout)
