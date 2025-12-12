from bs4 import BeautifulSoup, Tag
from typing import Dict, Any, Optional, Tuple, List
from urllib.parse import urljoin, urlparse

class WebParser:
    """
    网页解析器，使用BeautifulSoup辅助HTML解析
    """
    
    def __init__(self):
        """
        初始化网页解析器
        """
        pass
    
    def parse(self, html_content: str, config: Dict[str, Any]) -> Tuple[str, str]:
        """
        解析网页内容
        
        Args:
            html_content: 网页HTML内容
            config: 解析配置，包含title_selector、content_selector、exclude_selectors等
            
        Returns:
            (title, content_html): 标题和内容HTML
        """
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 获取标题
        title = self._extract_title(soup, config)
        
        # 获取内容
        content_html = self._extract_content(soup, config)
        
        return title, content_html
    
    def _extract_title(self, soup: BeautifulSoup, config: Dict[str, Any]) -> str:
        """
        提取网页标题
        
        Args:
            soup: BeautifulSoup对象
            config: 解析配置
            
        Returns:
            网页标题
        """
        title_selector = config.get("title_selector", "title")
        
        # 尝试使用CSS选择器提取标题
        title_element = soup.select_one(title_selector)
        if title_element:
            return title_element.get_text(strip=True)
        
        # 尝试从meta标签提取标题
        meta_title = soup.select_one("meta[name='title']")
        if meta_title and meta_title.get("content"):
            return meta_title["content"].strip()
        
        # 尝试从og:title提取标题
        og_title = soup.select_one("meta[property='og:title']")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()
        
        # 默认返回空字符串
        return ""
    
    def _extract_content(self, soup: BeautifulSoup, config: Dict[str, Any]) -> str:
        """
        提取网页内容
        
        Args:
            soup: BeautifulSoup对象
            config: 解析配置
            
        Returns:
            内容HTML
        """
        content_selector = config.get("content_selector", "body")
        exclude_selectors = config.get("exclude_selectors", ["script", "style", "nav", "footer"])
        
        # 复制原始soup，避免修改原对象
        content_soup = BeautifulSoup(str(soup), "html.parser")
        
        # 选择内容区域
        content_element = content_soup.select_one(content_selector)
        if not content_element:
            content_element = content_soup.body or content_soup
        
        # 移除需要排除的元素
        for selector in exclude_selectors:
            for element in content_element.select(selector):
                element.extract()
        
        # 清理内容，移除多余的空白和无用标签
        self._clean_content(content_element)
        
        # 返回处理后的HTML
        return str(content_element)
    
    def _clean_content(self, element: Tag) -> None:
        """
        清理内容，移除多余的空白和无用标签
        
        Args:
            element: 要清理的BeautifulSoup Tag对象
        """
        # 移除所有空标签
        for tag in element.find_all():
            if not tag.get_text(strip=True) and tag.name not in ["img", "br", "hr"]:
                tag.extract()
        
        # 移除多余的空白
        for text_node in element.find_all(text=True, recursive=True):
            if text_node.strip():
                text_node.replace_with(text_node.strip())
            else:
                text_node.extract()
    
    def extract_links(self, html_content: str, base_url: str) -> List[Dict[str, str]]:
        """
        提取网页中所有的a标签及其标题
        
        Args:
            html_content: 网页HTML内容
            base_url: 基础URL，用于处理相对URL
            
        Returns:
            List[Dict[str, str]]: 包含url和title字段的字典列表
        """
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 存储结果的列表
        links = []
        # 用于去重的集合
        seen_urls = set()
        
        # 遍历所有a标签
        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href", "").strip()
            
            # 跳过无效URL
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            
            # 处理相对URL，转换为绝对URL
            absolute_url = urljoin(base_url, href)
            
            # 跳过重复URL
            if absolute_url in seen_urls:
                continue
            seen_urls.add(absolute_url)
            
            # 提取标题
            title = ""
            
            # 1. 尝试从a标签的文本内容提取标题
            text = a_tag.get_text(strip=True)
            if text:
                title = text
            
            # 2. 如果没有文本内容，尝试从title属性提取
            if not title:
                title_attr = a_tag.get("title", "").strip()
                if title_attr:
                    title = title_attr
            
            # 3. 如果没有title属性，尝试从包含的img标签的alt属性提取
            if not title:
                img_tag = a_tag.find("img")
                if img_tag:
                    alt_text = img_tag.get("alt", "").strip()
                    if alt_text:
                        title = alt_text
                    # 或者从img标签的title属性提取
                    img_title = img_tag.get("title", "").strip()
                    if not title and img_title:
                        title = img_title
            
            # 4. 如果都没有，使用URL作为标题
            if not title:
                title = absolute_url
            
            # 添加到结果列表
            links.append({
                "url": absolute_url,
                "title": title
            })
        
        return links

# 创建全局解析器实例
web_parser = WebParser()
