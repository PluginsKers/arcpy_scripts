# -*- coding: utf-8 -*-

import arcpy
import arcpy.da
import re
import os
import sys


class ConvUnit:
    def __init__(self, _CONFIG):
        try:
            if os.path.exists(_CONFIG['argv'][1]):
                if _CONFIG['argv'][1].split(".")[-1] != "shp":
                    print(u"警告：无法解析传入文件")
                    sys.exit()
                # 程序开始
                print(u"开始加载.....部格式转换 Format TXT => 部格式TXT")
                __FRAME__ = u"[属性描述]"
                for el in re.findall(r"{input_(.+?)}", _CONFIG['frame_default']):
                    print(u"请输入项目[{}](不填为空)".format(el))
                    enter = raw_input("Enter: ").decode("utf8", "ignore")
                    _CONFIG['frame_default'] = _CONFIG['frame_default'].replace(
                        u"{{input_{}}}".format(el), enter)

                __FRAME__ += _CONFIG['frame_default']

                inFC = _CONFIG['argv'][1].decode("gbk", "ignore")
                fields = arcpy.ListFields(inFC)
                fields_array = ["SHAPE@"]
                for field in fields:
                    fields_array.append(field.aliasName)

                # 验证过程逻辑合法性
                for el in re.findall(r"{attr_(.+?)}", _CONFIG['frame_coordinate']):
                    if el in fields_array:
                        continue

                    else:
                        print(u"警告：SHP与TXT不匹配，请验证后继续")
                        sys.exit()

                # 解析TXT文件
                data = self.regular_input()

                __FRAME__ += u"[地块坐标]"

                # SHP解析游标
                with arcpy.da.SearchCursor(inFC, fields_array) as cursor:

                    for index, row in enumerate(cursor):
                        fr = _CONFIG['frame_coordinate']
                        fr = fr.replace(u"{{{}}}".format(
                            "Entries"), str(len(data[index]) - 1))
                        fr = fr.replace(u"{{{}}}".format("Area"), str(row[0].area))
                        fr = fr.replace(u"{{{}}}".format("No"), str(index + 1))

                        for el in re.findall(r"{attr_(.+?)}", fr):
                            fr = fr.replace(u"{{attr_{}}}".format(
                                el), row[fields_array.index(el)])

                        for o in data[index]:
                            fr += u"\nJ{},{},{},{}".format(o['index'],
                                                        o['type'], o['x'], o['y'])

                        __FRAME__ += fr

                with open(u"{}部格式.txt".format(_CONFIG['outdir']).decode("utf8", "ignore"), "w+") as f:
                    f.write(__FRAME__.replace("\r\n", "\n"))
                    print(u"文件已经保存为 {}{}".format(_CONFIG['outdir'], u"部格式.txt"))
            else:
                print(u"目标文件不存在")
        except Exception as e:
            print(e)

    def regular_input(self):
        try:
            input=open("input.txt", "rb")
            content=input.read().decode("utf8", "ignore")
            field_start_re=re.compile(
                r'^[0-9]\d* 0\r\n|^Polygon\r\n|^END', re.M)
            fields=re.split(field_start_re, content)
            a=[]
            for points in fields:
                if len(points) > 0:
                    b=[]
                    type=1
                    index=1
                    all=[]
                    for o in re.split(re.compile(r"\n|[\r\n]"), points):
                        if len(o) > 0:
                            all.append(o)

                    for i, point in enumerate(all):
                        if i is 0 or i is len(all) - 1:
                            index=1

                        if i is len(all) - 1:
                            next=point

                        else:
                            next=all[i + 1]

                        if re.search(re.compile(r'^InteriorRing', re.M), next):
                            index=1

                        if re.search(re.compile(r'^InteriorRing', re.M), point):
                            type=2
                            index=1

                        else:

                            c={}
                            column=point.split(" ")
                            c['x']=column[1]
                            c['y']=column[2]
                            c['type']=type
                            c['index']=index
                            index += 1

                            b.append(c)

                    a.append(b)

            return a

        except Exception as e:
            print(u"警告：在解析TXT文件时出现错误\n{}".format(e))
            sys.exit()
