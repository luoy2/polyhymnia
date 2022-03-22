import random

def random_deletion(words, p):
    '''
    # 随机删除: 以概率p删除语句中的词
    :param words:
    :param p:
    :return:
    '''
    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words) - 1)
        return [words[rand_int]]

    return new_words