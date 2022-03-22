import os
import requests
import hashlib
import json
import random
from retry import retry
import logging
from polyhymnia._logger import LoggingFactory


# 调用百度翻译API将中文翻译成英文
def baidu_translate(session, content, from_lang, to_lang):
    BAIDU_TRANSLATE_APPID = os.environ.get("BaiduAppId", None)
    BAIDU_TRANSLATE_KEY = os.environ.get("BaiduSecretKey", None)
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = content
    salt = random.randint(32768, 65536)
    sign = BAIDU_TRANSLATE_APPID + q + str(salt) + BAIDU_TRANSLATE_KEY
    sign = hashlib.md5(sign.encode()).hexdigest()
    r = session.get(url, params={"q": q,
                                 "from": from_lang,
                                 "to": to_lang,
                                 "appid": BAIDU_TRANSLATE_APPID,
                                 "salt": salt,
                                 "sign": sign,
                                 "action": 0
                                 })
    res = r.json()['trans_result'][0]['dst']
    # print(dst)  # 打印结果
    return res

@retry(tries=3, delay=1)
def gen(sentence, num_aug=8):
    '''
    对文字随机选择1-2种语言进行翻译，然后翻译回中文。 如zh -> en -> jp -> zh
    :param sentence:
    :param num_aug:
    :return:
    '''
    LoggingFactory.logger.debug(f"start translate for: {sentence}")
    session = requests.session()
    res = set()
    loop_cnt = 0
    max_loop = 3*num_aug # 翻译次数抵达3倍num_aug后强制结束
    while len(res) < num_aug and loop_cnt < max_loop:
        trans_loop_max = random.randint(1, 2)
        random_middle_lang = random.sample(
            ["en", "jp", "kor", "fra", "spa", "th", "ara", "ru", "pt", "de", "it", "el", "nl", "pl", "bul", "est",
             "dan", "fin", "cs", "rom", "slo", "swe", "hu"], trans_loop_max)
        trans = sentence
        prev_translan = 'zh'
        for trans_lan in random_middle_lang:
            trans = baidu_translate(session, trans, prev_translan, trans_lan)
            prev_translan = trans_lan
        translate_zh = baidu_translate(session, trans, prev_translan, 'zh')  # 中文翻译成英文
        LoggingFactory.logger.debug(f'zh -> {" -> ".join(random_middle_lang)} -> zh: {translate_zh}')
        res = res.union([translate_zh])
        loop_cnt += 1
    return list(res)


if __name__ == '__main__':
    contents = '贵金属矿采选'
    print(gen(contents, num_aug=3))

    # session = requests.session()
    # trans = "农业机械活动"
    # prev_translan = 'zh'
    # for trans_lan in  ["en", "jp", "kor", "fra", "spa", "th", "ara", "ru", "pt", "de", "it", "el", "nl", "pl", "bul", "est",
    #      "dan", "fin", "cs", "rom", "slo", "swe", "hu", "vie"]:
    #     trans = baidu_translate(session, trans, prev_translan, trans_lan)
    #     prev_translan = trans_lan
    #     translate_zh = baidu_translate(session, trans, prev_translan, 'zh')  # 中文翻译成英文
    #     LoggingFactory.logger.warning(f'zh -> {trans_lan} -> zh: {translate_zh}')
