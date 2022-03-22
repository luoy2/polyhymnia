import os
from pathlib import Path

INSTALLED_APPS = ["simbert", "aeda", "eda"]

# 百度翻译设置
BAIDU_TRANSLATE_APPID = os.environ.get("BaiduAppId", None)
BAIDU_TRANSLATE_KEY = os.environ.get("BaiduSecretKey", None)

# SIMBERT 模型位置
PRE_LM_PATH = Path("models") / 'chinese_roformer-sim-char-ft_L-6_H-384_A-6'