__all__ = ["StopWords"]

from sklearn.feature_extraction import text
import zhon.hanzi
import zhon.pinyin
import sys,os
import pathlib
folder_path = pathlib.Path(__file__).parents[1] / 'data'
stop_words_path = folder_path


StopWords = set()
with open(f'{folder_path}/stopwords/baidu_stopwords.txt', 'r', encoding='utf8') as f:
    stop_words = f.readlines()
StopWords = StopWords.union([i.strip() for i in stop_words])

with open(f'{folder_path}/stopwords/cn_stopwords.txt', 'r', encoding='utf8') as f:
    stop_words = f.readlines()
StopWords = StopWords.union([i.strip() for i in stop_words])

with open(f'{folder_path}/stopwords/hit_stopwords.txt', 'r', encoding='utf8') as f:
    stop_words = f.readlines()
StopWords = StopWords.union([i.strip() for i in stop_words])

with open(f'{folder_path}/stopwords/scu_stopwords.txt', 'r', encoding='utf8') as f:
    stop_words = f.readlines()
StopWords = StopWords.union([i.strip() for i in stop_words])
StopWords = StopWords.union(list(text.ENGLISH_STOP_WORDS))
StopWords = StopWords.union([i for i in zhon.pinyin.punctuation + zhon.hanzi.punctuation])
StopWords = StopWords.union([' ', '\u3000'])
StopWords = list(StopWords)
