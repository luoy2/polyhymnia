__all__ = ['get_synonyms']
import os
import pathlib
# os.environ["SYNONYMS_WORD2VEC_BIN_MODEL_ZH_CN"] = str(pathlib.Path(__file__).parents[1] / 'data/words.vector')
import synonyms


def get_synonyms(word):
    return synonyms.nearby(word)[0]
