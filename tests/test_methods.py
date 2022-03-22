import unittest
import logging

logging.basicConfig()
import polyhymnia
polyhymnia.set_verbose(True)
from pprint import pprint

from polyhymnia import Simbert
from polyhymnia import EDA
from polyhymnia import AEDA
from polyhymnia import ReverseTranslate



class TestMethods(unittest.TestCase):

    def test_simbert(self):
        result = Simbert.gen("身份证丢了怎么办", 8)
        pprint(result)
        assert result



    def test_reverse_translate(self):
        try:
            result = ReverseTranslate.gen("小麦种植", 4)
            pprint(result)
            assert result
        except EnvironmentError as e:
            print(e)



    def test_eda(self):
        result = EDA.gen("小麦种植", 8)
        pprint(result)
        assert result


    def test_aeda(self):
        result = AEDA.gen("身份证丢了怎么办", num_aug=4)
        pprint(result)
        assert result


if __name__ == '__main__':
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--appid', type=str, help='baidu translate app id')
    # parser.add_argument('--secret', type=str, help='baidu translate app secret')
    # FLAGS, unparsed = parser.parse_known_args()
    # if getattr(FLAGS, 'appid', None) and getattr(FLAGS, 'secret', None):
    #     ReverseTranslate.set_creds(FLAGS.appid, FLAGS.secret)
    unittest.main()