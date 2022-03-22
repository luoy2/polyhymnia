import random
from polyhymnia.utils.synonyms import get_synonyms
from polyhymnia.utils.stop_words import StopWords

def synonym_replacement(words, n):
    '''
    同义词替换 替换一个语句中的n个单词为其同义词
    :param words:
    :param n:
    :return:
    '''
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in StopWords]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(synonyms)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break

    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')

    return new_words