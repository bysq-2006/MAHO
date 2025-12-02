import argostranslate.package
import argostranslate.translate
from langdetect import detect
import logging


class Client:
    """
    Argos Translate 离线翻译客户端，自动识别源语言并翻译。
    """

    def __init__(self, **kwargs):
        # 支持配置目标语言，默认日语
        self.to_lang = kwargs.get("to_lang", "ja")
        self.model_installed = False
        self.translate("你好")  # 预加载模型

    def _ensure_model(self, from_lang, to_lang):
        """尝试加载或下载模型，支持动态语言对"""
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        try:
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_lang and x.to_code == to_lang, available_packages
                )
            )
            argostranslate.package.install_from_path(
                package_to_install.download())
            logging.info(f"Argos Translate: 已加载 {from_lang} 到 {to_lang} 的模型包。")
            return True
        except StopIteration:
            logging.warning(f"Argos Translate: 未找到 {from_lang} 到 {to_lang} 的模型包。")
            return False

    def translate(self, text: str, from_lang: str = '', to_lang: str = 'ja') -> str:
        # 处理空文本
        if not text or not text.strip():
            logging.warning("翻译文本为空，返回原文")
            return text
        
        # 自动检测源语言
        if not from_lang:
            try:
                from_lang = detect(text)
            except Exception as e:
                logging.warning(f"语言检测失败: {e}，返回原文")
                return text
        
        if not to_lang:
            to_lang = self.to_lang
        
        # 尝试加载模型，若失败则返回原文
        if not self._ensure_model(from_lang, to_lang):
            logging.warning(f"无法加载 {from_lang} 到 {to_lang} 的模型，返回原文")
            return text
        
        try:
            return argostranslate.translate.translate(text, from_lang, to_lang)
        except Exception as e:
            logging.error(f"翻译失败: {e}，返回原文")
            return text
