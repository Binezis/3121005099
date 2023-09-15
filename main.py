import math
import sys
import jieba.analyse

import jieba


def subWord(text):
    file = open(text, 'r', encoding='utf-8')
    seg_text = file.read()
    words_len = len(list(jieba.lcut(seg_text)))
    top_k = math.ceil(0.08 * words_len)
    # top_k为下面extract_tags()中参数topK的值，因为每篇文章不同，所以没有设置固定的参数值
    words = jieba.analyse.extract_tags(seg_text, topK=top_k)
    file.close()
    return words


def main():
    """

    :return:
    """
    orig_path = sys.argv[1]
    copy_path = sys.argv[2]
    result_path = sys.argv[3]
    if len(sys.argv) != 4:
        print('输入格式为：python main.py [原文文件] [抄袭版论文的文件] [答案文件]')
    orig_keyword = subWord(orig_path)
    copy_keyword = subWord(copy_path)


if __name__ == '__main__':
    main()
