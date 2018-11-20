# 启动文件
import os
import sys
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH)

from core import main


if __name__ == '__main__':
    main.ArgvHandler()
