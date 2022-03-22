import random

def random_swap(words, n):
    '''
     Random swap: Randomly swap two words in the sentence n times
    :param words:
    :param n:
    :return:
    '''
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words


def swap_word(new_words):
    if len(new_words) < 2:
        return new_words
    start_idx = 0
    end_idx = len(new_words) - 1
    random_idx_1 = random.randint(start_idx, end_idx)
    if random_idx_1 == 0:
        random_idx_2 = 1
    elif random_idx_1 == len(new_words) - 1:
        random_idx_2 = random_idx_1 - 1
    else:
        random_idx_2 = random_idx_1 + (-1) ** random.randint(0, 1)
    # print(random_idx_1, random_idx_2)
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    return new_words
