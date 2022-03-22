import math
import logging
import jieba
import random
from random import shuffle
from polyhymnia.methods.noising.deletion import random_deletion
from polyhymnia.methods.noising.swapping import random_swap
from polyhymnia.methods.noising.insertion import random_insertion
from polyhymnia.methods.noising.substitution import synonym_replacement
from polyhymnia._logger import LoggingFactory

from scipy.stats import qmc
from collections import Counter

sampler = qmc.Sobol(d=2, scramble=False)

def gen(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):
    '''

    :param sentence: 句子
    :param alpha_sr: 同义词替换概率
    :param alpha_ri: 随机插入概率
    :param alpha_rs: 随机替换词顺序概率
    :param p_rd: 随机删除概率
    :param num_aug:
    :return:
    '''
    seg_list = jieba.cut(sentence)
    seg_list = " ".join(seg_list)
    words = list(seg_list.split())
    num_words = len(words)

    n_sr = max(1, int(alpha_sr * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))

    tasks_lists = []
    if alpha_ri > 0:
        tasks_lists.append((random_insertion, n_ri))
    if alpha_rs > 0:
        tasks_lists.append((random_swap, n_rs))
    if alpha_sr > 0:
        tasks_lists.append((synonym_replacement, n_sr))
    if p_rd > 0:
        tasks_lists.append((random_deletion, p_rd))

    task_sequence = [int(i[0]*len(tasks_lists)) for i in sampler.random(num_aug)]
    counter = Counter(task_sequence)
    LoggingFactory.logger.debug("execute tasks: ")
    for k,v in counter.items():
        LoggingFactory.logger.debug(f"{tasks_lists[k][0].__name__}: {v} times")


    augmented_sentences = []
    for task_id in task_sequence:
        task_to_execute, task_arg = tasks_lists[task_id]
        a_words = task_to_execute(words, task_arg)
        augged_sent = "".join(a_words)
        LoggingFactory.logger.debug(f"{task_to_execute.__name__} --- {augged_sent}")
        augmented_sentences.append(augged_sent)

    shuffle(augmented_sentences)

    return augmented_sentences


if __name__ == '__main__':
    from polyhymnia.methods.noising.stacking.eda import gen
    contents = '小麦种植'
    print(gen(contents, num_aug=8, p_rd=0, alpha_ri=0))