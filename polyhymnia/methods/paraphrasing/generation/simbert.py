#! -*- coding: utf-8 -*-
import os
os.environ["TF_KERAS"] = "1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import numpy as np
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
try:
    assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except Exception as e:
    pass
from bert4keras.snippets import AutoRegressiveDecoder
from bert4keras.backend import keras, K
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer, load_vocab
from bert4keras.snippets import sequence_padding
import pathlib
import logging
import zipfile

DATA_PATH = pathlib.Path(__file__).parents[3] / 'data'
PRE_LM_PATH = pathlib.Path(__file__).parents[3] / 'model/chinese_roformer-sim-char-ft_L-6_H-384_A-6'
# print(DATA_PATH.absolute())
# print(PRE_LM_PATH.absolute())
config_path = str(PRE_LM_PATH / 'bert_config.json')
checkpoint_path = str(PRE_LM_PATH / 'bert_model.ckpt')
dict_path = str(PRE_LM_PATH / 'vocab.txt')

if not pathlib.Path(dict_path).exists():
    logging.warning("unzip simbert model...")
    PRE_LM_PATH.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(DATA_PATH / 'simbert_v2_small.zip'), 'r') as zip_ref:
        zip_ref.extractall(str(PRE_LM_PATH.parent.absolute()))

maxlen = 64

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器

# 建立加载模型
roformer = build_transformer_model(
    config_path,
    checkpoint_path,
    model='roformer',
    application='unilm',
    with_pool='linear'
)

encoder = keras.models.Model(roformer.inputs, roformer.outputs[0])
seq2seq = keras.models.Model(roformer.inputs, roformer.outputs[1])


class SynonymsGenerator(AutoRegressiveDecoder):
    """seq2seq解码器
    """

    @AutoRegressiveDecoder.wraps(default_rtype='probas')
    def predict(self, inputs, output_ids, step):
        token_ids, segment_ids = inputs
        token_ids = np.concatenate([token_ids, output_ids], 1)
        segment_ids = np.concatenate([segment_ids, np.ones_like(output_ids)], 1)
        return self.last_token(seq2seq).predict([token_ids, segment_ids])

    def generate(self, text, n=1, topp=0.95, mask_idxs=[]):
        token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
        for i in mask_idxs:
            token_ids[i] = tokenizer._token_mask_id
        output_ids = self.random_sample([token_ids, segment_ids], n,
                                        topp=topp)  # 基于随机采样
        return [tokenizer.decode(ids) for ids in output_ids]


synonyms_generator = SynonymsGenerator(
    start_id=None, end_id=tokenizer._token_end_id, maxlen=maxlen
)


def gen(text, num_aug=4):
    ''''含义： 产生sent的n个相似句，然后返回最相似的k个。
    做法：用seq2seq生成，并用encoder算相似度并排序。
    '''
    n = max(num_aug * 5, 30)
    mask_idxs = []
    k = num_aug
    r = synonyms_generator.generate(text, n, mask_idxs=mask_idxs)
    r = [i for i in set(r) if i != text]
    r = [text] + r
    X, S = [], []
    for t in r:
        x, s = tokenizer.encode(t)
        X.append(x)
        S.append(s)
    X = sequence_padding(X)
    S = sequence_padding(S)
    Z = encoder.predict([X, S])
    Z /= (Z ** 2).sum(axis=1, keepdims=True) ** 0.5
    argsort = np.dot(Z[1:], -Z[0]).argsort()
    return [r[i + 1] for i in argsort[:k]]


if __name__ == '__main__':
    print(gen('我们就像蒲公英，我也祈祷着能和你飞去同一片土地', 8))
