import hashlib
import math
import re
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


def get_similarity(orig_hash, copy_hash):
    distance = 0
    if len(orig_hash) != len(copy_hash):
        distance = -1
    else:
        for i in range(len(orig_hash)):
            if orig_hash[i] != copy_hash[i]:
                distance += 1
    similarity = 0.01 * (100 - distance * 100 / 128)
    return similarity


def subWord(text):
    file = open(text, 'r', encoding='utf-8')
    seg_text = file.read()
    # 正则表达式过滤只剩中文
    pattern = re.compile(u"[^\u4e00-\u9fa5]")
    seg_text = pattern.sub("", seg_text)
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

    try:
        orig_path: str = sys.argv[1]
        copy_path: str = sys.argv[2]
        result_path: str = sys.argv[3]
    except IndexError:
        print('输入格式错误,正确格式为为：python main.py [原文文件] [抄袭版论文的文件] [答案文件]')
        return IndexError
    try:
        orig_keyword = subWord(orig_path)
        copy_keyword = subWord(copy_path)
    except FileNotFoundError:
        print("文件地址错误，找不到文件，")
        return FileNotFoundError
    orig_simhash = getSimhash(orig_keyword)
    copy_simhash = getSimhash(copy_keyword)
    similarity = get_similarity(orig_simhash, copy_simhash)
    try:
        result_file = open(result_path, 'w', encoding='utf-8')
    except (FileNotFoundError, PermissionError):
        print('输出文件路径错误')
        return FileNotFoundError, PermissionError
    result_file.write('相似度:' + str(similarity))
    result_file.close()
    print('相似度:%f' % similarity)


if __name__ == '__main__':
    main()
