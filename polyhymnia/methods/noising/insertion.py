import random
import math
from polyhymnia.utils.synonyms import get_synonyms


def random_insertion(words, n):
    '''
    随机插入: 随机在语句中插入n个词
    :param words:
    :param n:
    :return:
    '''
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words


def add_word(new_words):
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words) - 1)]
        synonyms = get_synonyms(random_word)
        counter += 1
        if counter >= 10:
            return
    random_synonym = random.choice(synonyms)
    random_idx = random.randint(0, len(new_words) - 1)
    new_words.insert(random_idx, random_synonym)


def aeda_text(s, fraction=1 / 3, puncs=None):
    if puncs is None:
        puncs = [",", "。", "，", "\t", " "]
    no_puncs = random.randint(0, math.ceil(len(s) * fraction))
    punc_to_be_inserted = random.choices(puncs,
                                         k=no_puncs)
    s = list(s)
    for p in punc_to_be_inserted:
        s.insert(random.randint(0, len(s)), p)
    s = "".join(s)
    return s
