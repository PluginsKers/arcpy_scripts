# -*- coding: utf-8 -*-

import arcpy
import arcpy.da
import re
import os
import sys

reload(sys)
sys.setdefaultencoding("utf8")

__CONFIG__ = {
    "version": "1.0.7",
    "frame": "config.txt".decode("utf8", "ignore"),
    "outfile": "部格式.txt".decode("utf8", "ignore"),
}
__PATH__ = (sys.path[0] + "\\..\\").decode("utf8", "ignore")
__FRAME__ = ""


print("__________.__               .__               ____  __.                   \n\\______   \\  |  __ __  ____ |__| ____   _____|    |/ _|___________  ______\n |     ___/  | |  |  \\/ ___\\|  |/    \\ /  ___/      <_/ __ \\_  __ \\/  ___/\n |    |   |  |_|  |  / /_/  >  |   |  \\\\___ \\|    |  \\  ___/|  | \\/\\___ \\ \n |____|   |____/____/\\___  /|__|___|  /____  >____|__ \\___  >__|  /____  >\n                    /_____/         \\/     \\/        \\/   \\/           \\/ \n--------------------------------------------------------------------------")
print(
    u"开始加载...请稍后，项目文件过大可能需要的时间很长\n如果堆栈出现错误，可以使用Ctrl+c强制退出\n程序当前版本: {0}\nArcGIS内核版本: {1}\nPython版本: {2}\n操作系统: {3}\nGithub开源地址: https://github.com/PluginsKers/ArcPy_Scripts\n--------------------------------------------------------------------------".format(__CONFIG__['version'], arcpy.GetInstallInfo()['Version'], sys.version, sys.platform))

# 读取基础框架信息
f = open(u"{0}{1}".format(__PATH__, __CONFIG__['frame']), "rb")
_frame = re.split("\[.*\]", f.read().decode("utf8", "ignore"))
frame_default = _frame[1]
frame_coordinate = _frame[2]

for el in re.findall(r"{input_(.+?)}", frame_default):
    print(u"请输入项目[{}](不填为空)".format(el))
    enter = raw_input("Enter: ")
    frame_default = frame_default.replace(u"{{input_{}}}".format(el), enter)

__FRAME__ += u"[属性描述]"
__FRAME__ += frame_default

print(u"开始加载主程序.....")


def regular_output():
    try:
        output = open("output.txt", "rb")
        content = output.read().decode("utf8", "ignore")
        field_start_re = re.compile(r'^[0-9]\d* 0\r\n|^Polygon\r\n|^END', re.M)
        fields = re.split(field_start_re, content)
        a = []
        for points in fields:
            if len(points) > 0:
                b = []
                type = 1
                index = 1
                all = []
                for o in re.split(re.compile(r"\n|[\r\n]"), points):
                    if len(o) > 0:
                        all.append(o)

                for i, point in enumerate(all):
                    if i is 0 or i is len(all) - 1:
                        index = 1

                    if i is len(all) - 1:
                        next = point

                    else:
                        next = all[i + 1]

                    if re.search(re.compile(r'^InteriorRing', re.M), next):
                        index = 1

                    if re.search(re.compile(r'^InteriorRing', re.M), point):
                        type = 2
                        index = 1

                    else:

                        c = {}
                        column = point.split(" ")
                        c['x'] = column[1]
                        c['y'] = column[2]
                        c['type'] = type
                        c['index'] = index
                        index += 1

                        b.append(c)

                a.append(b)

        return a

    except Exception, e:
        print(u"警告：在解析TXT文件时出现错误\n{}".format(e))
        sys.exit()


if os.path.exists(sys.argv[1]):
    # 程序开始
    inFC = sys.argv[1].decode("gbk", "ignore")
    fields = arcpy.ListFields(inFC)
    fields_array = ["SHAPE@"]
    for field in fields:
        fields_array.append(field.aliasName)

    # 验证过程逻辑合法性
    for el in re.findall(r"{attr_(.+?)}", frame_coordinate):
        if el in fields_array:
            continue

        else:
            print(u"警告：SHP与TXT不匹配，请验证后继续")
            sys.exit()

    # 解析TXT文件
    data = regular_output()

    __FRAME__ += u"[地块坐标]"

    # SHP解析游标
    with arcpy.da.SearchCursor(inFC, fields_array) as cursor:

        for index, row in enumerate(cursor):
            fr = frame_coordinate
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

    with open(__CONFIG__['outfile'], "w+") as f:
        f.write(__FRAME__.replace("\r\n", "\n"))
        print(u"文件已经保存为 {}".format(__CONFIG__['outfile']))


else:
    print(u"目标文件不存在")
