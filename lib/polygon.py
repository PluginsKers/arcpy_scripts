# -*- coding: utf-8 -*-

import arcpy
import arcpy.da
import re
import os
import sys
import chardet


class ConvPolygon:
    def __init__(self, _CONFIG):
        print(u"开始加载.....几何文件构造 部格式TXT => 几何SHP")
        if os.path.exists(_CONFIG['argv'][1]):
            if _CONFIG['argv'][1].split(".")[-1] != "txt":
                print(u"警告：无法解析传入文件")
                sys.exit()

            input = open(_CONFIG['argv'][1], "rb")
            content = input.read().replace("\r\n", "\n")
            for a in re.split(r"^(.+?)@", re.split(r"\[.*\]", content)[2], 0, re.M):
                if len(a) > 3:
                    print(chardet.detect(a))
                    print(a)

        else:
            print(u"目标文件不存在")
