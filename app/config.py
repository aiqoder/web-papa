import os
import yaml
from typing import Dict, Any, Optional

class ConfigManager:
    """
    配置管理类，负责加载和管理网站特定的解析配置
    """
    
    def __init__(self, config_dir: str = "configs"):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置文件目录，默认为"configs"
        """
        self.config_dir = config_dir
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.default_config: Dict[str, Any] = {}
        
        # 加载所有配置文件
        self.load_configs()
    
    def load_configs(self):
        """
        加载所有配置文件到内存
        """
        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # 遍历配置目录下的所有YAML文件
        for filename in os.listdir(self.config_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                config_name = os.path.splitext(filename)[0]
                config_path = os.path.join(self.config_dir, filename)
                
                # 加载配置文件
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    self.configs[config_name] = config
        
        # 设置默认配置
        self.default_config = self.configs.get("default", {
            "title_selector": "title",
            "content_selector": "body",
            "exclude_selectors": ["script", "style", "nav", "footer"]
        })
    
    def get_config(self, config_name: Optional[str] = None, url: Optional[str] = None) -> Dict[str, Any]:
        """
        获取配置
        
        Args:
            config_name: 配置名称，如"default"、"wechat"
            url: 目标URL，用于根据域名自动匹配配置
            
        Returns:
            配置字典
        """
        # 如果指定了配置名称，直接返回对应配置
        if config_name and config_name in self.configs:
            return self.configs[config_name]
        
        # 如果提供了URL，尝试根据域名匹配配置
        if url:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # 域名到配置名称的映射
            domain_mapping = {
                "www.right.com.cn": "80211",
                "right.com.cn": "80211",
                "www.52pojie.cn": "52pojie",
                "52pojie.cn": "52pojie",
                "juejin.cn": "juejin",
                "www.juejin.cn": "juejin",
                "csdn.net": "csdn",
                "www.csdn.net": "csdn",
                "zhihu.com": "zhihu",
                "www.zhihu.com": "zhihu",
                "mp.weixin.qq.com": "wechat"
            }
            
            # 检查域名映射
            if domain in domain_mapping:
                mapped_config_name = domain_mapping[domain]
                if mapped_config_name in self.configs:
                    return self.configs[mapped_config_name]
            
            # 尝试匹配完整域名
            if domain in self.configs:
                return self.configs[domain]
            
            # 尝试匹配顶级域名
            parts = domain.split(".")
            if len(parts) >= 2:
                tld = ".".join(parts[-2:])
                # 检查顶级域名映射
                if tld in domain_mapping:
                    mapped_config_name = domain_mapping[tld]
                    if mapped_config_name in self.configs:
                        return self.configs[mapped_config_name]
                
                # 尝试直接匹配顶级域名
                if tld in self.configs:
                    return self.configs[tld]
        
        # 返回默认配置
        return self.default_config

# 创建全局配置管理器实例
config_manager = ConfigManager()
