from polyhymnia._logger import LoggingFactory
import os

def set_verbose(v):
    return LoggingFactory.set_verbose(v)


class Simbert:
    _has_compiled = None

    @classmethod
    def gen(cls, text, num_aug):
        from polyhymnia.methods.paraphrasing.generation.simbert import gen as gen_simbert
        if not cls._has_compiled:
            cls._has_compiled = True
        return gen_simbert(text, num_aug)


class ReverseTranslate:
    _has_compiled = None

    @classmethod
    def gen(cls, text, num_aug):
        from polyhymnia.methods.paraphrasing.translation.baidu import gen as reverse_translate
        if not cls._has_compiled:
            BAIDU_TRANSLATE_APPID = os.environ.get("BaiduAppId", None)
            BAIDU_TRANSLATE_KEY = os.environ.get("BaiduSecretKey", None)
            if BAIDU_TRANSLATE_APPID is None or BAIDU_TRANSLATE_KEY is None:
                raise EnvironmentError("请使用 ReverseTranslate.set_creds(appid, appSecret) 设置百度API密钥！")
            cls._has_compiled = True
        return reverse_translate(text, num_aug)

    @staticmethod
    def set_creds(appid, appSecret):
        os.environ["BaiduAppId"] = appid
        os.environ["BaiduSecretKey"] = appSecret


class EDA:
    _has_compiled = None

    @classmethod
    def gen(cls, text, num_aug):
        from polyhymnia.methods.noising.stacking.eda import gen as eda
        if not cls._has_compiled:
            cls._has_compiled = True
        return eda(text, num_aug=num_aug)

class AEDA:
    _has_compiled = None

    @classmethod
    def gen(cls, text, num_aug):
        from polyhymnia.methods.noising.insertion import aeda_text
        if not cls._has_compiled:
            cls._has_compiled = True
        texts = []
        for _ in range(num_aug):
            texts.append(aeda_text(text))
        return texts
