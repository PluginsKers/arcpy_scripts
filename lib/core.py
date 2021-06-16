# -*- coding: utf-8 -*-

import arcpy
import arcpy.da
import re
import os
import sys
import unit
# import polygon

if __name__ == '__main__':
    __PATH__ = (sys.path[0] + "\\..\\").decode("utf8", "ignore")

    '''
    读取基础框架信息
    '''
    f = open(u"{0}{1}".format(__PATH__, "config.txt"), "rb")
    _frame = re.split(r"\[.*\]", f.read().decode("utf8",
                      "ignore").replace("\r\n", "\n").replace("\r", "\n"))
    frame_default = u""
    frame_coordinate = u""
    for line in _frame[1]:
        if len(line) > 0:
            frame_default += line

    for line in re.split(r"^(.*)\n", _frame[1], 0, re.M):
        if len(line) > 0:
            frame_coordinate += line

    '''
    全局变量设置
    '''
    _CONFIG = {
        "version": "1.0.8",
        "outdir": "./dist/",
        "frame_default": frame_default,
        "frame_coordinate": frame_coordinate,
        "path": __PATH__,
        "argv": sys.argv,
    }

    print(u"__________.__               .__               ____  __.                   \n\\______   \\  |  __ __  ____ |__| ____   _____|    |/ _|___________  ______\n |     ___/  | |  |  \\/ ___\\|  |/    \\ /  ___/      <_/ __ \\_  __ \\/  ___/\n |    |   |  |_|  |  / /_/  >  |   |  \\\\___ \\|    |  \\  ___/|  | \\/\\___ \\ \n |____|   |____/____/\\___  /|__|___|  /____  >____|__ \\___  >__|  /____  >\n                    /_____/         \\/     \\/        \\/   \\/           \\/ \n--------------------------------------------------------------------------")
    print(
        u"开始加载...请稍后，项目文件过大可能需要的时间很长\n如果堆栈出现错误，可以使用Ctrl+c强制退出\n程序当前版本: {}\nArcGIS内核版本: {}\nPython解释器版本: {}\n操作系统: {}\nGithub开源地址: https://github.com/PluginsKers/ArcPy_Scripts\n--------------------------------------------------------------------------".format(_CONFIG['version'], arcpy.GetInstallInfo()['Version'], sys.version, sys.platform))

    print(u"选择你希望加载的模块（功能）\n1. 部格式转换 Format TXT => 部格式TXT\n2. 几何文件构造 部格式TXT => 几何SHP")
    switch = raw_input("Enter: ")
    os.system('cls')
    if switch is "1":
        unit.ConvUnit(_CONFIG)
    # elif switch is "2":
    #     polygon.ConvPolygon(_CONFIG)
    else:
        print(u"警告：请填写正确的信息")
