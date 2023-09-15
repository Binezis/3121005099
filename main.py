import hashlib
import math
import sys
import jieba.analyse
import jieba


def getSimhash(keyword):
    vector = [0] * 128
    i = 0
    size = len(keyword)
    for word in keyword:
        # 利用MD5获得字符串的hash值
        md5 = hashlib.md5()
        md5.update(word.encode("utf-8"))
        hash_value = bin(int(md5.hexdigest(), 16))[2:]
        if len(hash_value) < 128:  # hash值少于128位，需在低位以0补齐
            dif = 128 - len(hash_value)
            for d in range(dif):
                hash_value += '0'
        # 加权 合并
        for j in range(len(vector)):  # 加权：权重由词频决定，从高到低分别是10 -> 0
            if hash_value[j] == '1':
                vector[j] += (10 - (i / (size / 10)))
            else:
                vector[j] -= (10 - (i / (size / 10)))
        i += 1
    # 降维
    simhash_value = ''
    for x in range(len(vector)):
        if vector[x] >= 0:  # 对特征向量的每一位进行遍历，大于0置1，小于0置0
            simhash_value += '1'
        else:
            simhash_value += '0'
    return simhash_value


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
    orig_simhash = getSimhash(orig_keyword)
    copy_simhash = getSimhash(copy_keyword)
    print(orig_simhash, copy_simhash)


if __name__ == '__main__':
    main()
