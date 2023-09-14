import sys


def main():
    """

    :return:
    """
    orig_path = sys.argv[1]
    copy_path = sys.argv[2]
    result_path = sys.argv[3]
    if len(sys.argv) != 4:
        print('输入格式为：python main.py [原文文件] [抄袭版论文的文件] [答案文件]')


if __name__ == '__main__':
    main()
