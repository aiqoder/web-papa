import markdownify
from typing import Optional

class MarkdownConverter:
    """
    Markdown转换器，将HTML内容转换为Markdown格式
    """
    
    def __init__(self):
        """
        初始化Markdown转换器
        """
        # 配置markdownify选项
        self.options = {
            "heading_style": "ATX",  # 使用#号风格的标题
            "code_language": None,    # 代码块语言
            "wrap_width": 80,         # 行宽限制
            "autolinks": True,        # 自动识别链接
            "bullet_list_marker": "-",  # 无序列表使用-标记
            "strong_em_symbol": "*",    # 粗体和斜体使用*符号
        }
    
    def convert(self, html_content: str, title: Optional[str] = None) -> str:
        """
        将HTML内容转换为Markdown格式
        
        Args:
            html_content: HTML内容
            title: 可选的标题，会添加到Markdown内容开头
            
        Returns:
            Markdown格式的内容
        """
        # 使用markdownify转换HTML
        md_content = markdownify.markdownify(html_content, **self.options)
        
        # 如果提供了标题，添加到内容开头
        if title:
            # 确保标题格式正确
            title = title.strip()
            # 如果标题没有以#开头，添加一级标题标记
            if not title.startswith("#"):
                md_content = f"# {title}\n\n{md_content}"
        
        # 清理转换后的内容
        md_content = self._clean_markdown(md_content)
        
        return md_content
    
    def _clean_markdown(self, md_content: str) -> str:
        """
        清理转换后的Markdown内容，确保格式规范
        
        Args:
            md_content: 转换后的Markdown内容
            
        Returns:
            清理后的Markdown内容
        """
        lines = []
        
        # 遍历每一行，清理多余的空白和空行
        for line in md_content.splitlines():
            stripped_line = line.rstrip()
            
            # 只添加非空行，或者保留必要的空行
            if stripped_line:
                lines.append(stripped_line)
            else:
                # 避免连续的空行
                if not lines or lines[-1]:
                    lines.append("")
        
        # 移除末尾的空行
        while lines and not lines[-1]:
            lines.pop()
        
        # 重新组合内容
        cleaned_content = "\n".join(lines)
        
        return cleaned_content
    
    def convert_title(self, title: str) -> str:
        """
        转换标题为Markdown格式
        
        Args:
            title: 原始标题
            
        Returns:
            Markdown格式的标题
        """
        title = title.strip()
        if not title.startswith("#"):
            return f"# {title}"
        return title

# 创建全局转换器实例
markdown_converter = MarkdownConverter()
