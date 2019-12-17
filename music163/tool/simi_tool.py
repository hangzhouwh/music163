# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 20:00
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : simi_tool.py 
# @Software: PyCharm

from gensim.models import KeyedVectors
import numpy as np




# 未知词、短语向量补齐
def compute_ngrams(word, min_n, max_n):
    extended_word = word
    ngrams = []
    for ngram_length in range(min_n, min(len(extended_word), max_n) + 1):
        for i in range(0, len(extended_word) - ngram_length + 1):
            ngrams.append(extended_word[i:i + ngram_length])
    return list(set(ngrams))


def wordVec(word, wv_from_text, min_n=1, max_n=3):
    # 确认词向量维度
    word_size = wv_from_text.wv.syn0[0].shape[0]
    # 计算word的ngrams词组
    ngrams = compute_ngrams(word, min_n=min_n, max_n=max_n)
    # 如果在词典之中，直接返回词向量
    if word in wv_from_text.wv.vocab.keys():
        return wv_from_text[word]
    else:
        # 不在词典的情况下
        word_vec = np.zeros(word_size, dtype=np.float32)
        ngrams_found = 0
        ngrams_single = [ng for ng in ngrams if len(ng) == 1]
        ngrams_more = [ng for ng in ngrams if len(ng) > 1]
        # 先只接受2个单词长度以上的词向量
        for ngram in ngrams_more:
            if ngram in wv_from_text.wv.vocab.keys():
                word_vec += wv_from_text[ngram]
                ngrams_found += 1
                # print(ngram)
        # 如果，没有匹配到，那么最后是考虑单个词向量
        if ngrams_found == 0:
            for ngram in ngrams_single:
                word_vec += wv_from_text[ngram]
                ngrams_found += 1
        if word_vec.any():
            return word_vec / max(1, ngrams_found)
        else:
            raise KeyError('all ngrams for word %s absent from model' % word)


if __name__ == "__main__":
	file = './data/Tencent_AILab_ChineseEmbedding.txt'
	wv_from_text = KeyedVectors.load_word2vec_format(file, binary=False)