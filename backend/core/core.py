from core.config import Config


class BaseAmadeus:
    """
        Amadeus核心类，负责初始化和管理核心功能
    """
    def __init__(self):
        self.config = Config('config.yaml').config
        print("Configuration loaded:", self.config)
