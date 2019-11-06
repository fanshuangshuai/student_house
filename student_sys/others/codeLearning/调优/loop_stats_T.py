# coding=utf-8
import cProfile
import pstats       # 用于打印关于已分析的python代码的报告的类。
from io import StringIO

pr = cProfile.Profile()     # 使用指定的计时器函数构建分析器对象。


def loop(count):
    result = []
    for i in range(count):
        result.append(i)

pr.enable()     # 开始收集分析信息
loop(100000)
pr.disable()    # 停止收集分析信息
s = StringIO()
# sortby = 'cumulative'
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())     # 检索对象的全部内容。
