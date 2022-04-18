import time

market_dic = {
    "安徽":[95,165,229,100,28,198,135,46,156,128],
    "北京":[4,2,18,9],
    "重庆":[244],
    "福建":[26,98,139],
    "甘肃":[51,237,104,82,94],
    "广东":[233,99,11],
    "广西":[232,169],
    "贵州":[242,243,174],
    "河北":[85,71,48,121,36,141,17,20,201],
    "黑龙江":[21,227],
    "河南":[159,120,70,216,109,221],
    "湖北":[29,90,230,47,231,7,124,37],
    "湖南":[113,80,136,72,116],
    "江苏":[50,125,1,6,75,32,68],
    "江西":[27,23,142,110],
    "吉林":[193],
    "辽宁":[63,34,129,44,16],
    "内蒙古":[84,5,73,45],
    "宁夏":[217],
    "青藏":[223],
    "陕西":[83,10],
    "山东":[61,111,56,226,170,155,219,160,115,52,194,66,162,106,122,33,60],
    "上海":[76,228],
    "山西":[19,88,119,25,54,114,143,30,10,140,101,97,103],
    "四川":[147,108,117,149,62,67],
    "天津":[49,77,41,65,146,38],
    "新疆":[8,31,236,79,137,118,69],
    "云南":[53,92,179],
    "浙江":[189,59,13,57,123,22]
}

from new_agricultural.Spider import CurrentSpider
# from new_agricultural.dounan import CurrentSpider as dn
# dn()
# for key in market_dic:
#     for i in market_dic.get(key):
#         CurrentSpider.enterMethod(i)
#         time.sleep(5)
#         break
#     break

#水果
from new_agricultural.shangwu.shuiguo import CurrentSpider as sgc
sgc()
#蔬菜
from new_agricultural.shangwu.shucai import CurrentSpider as scc
scc()
#食用菌
from new_agricultural.shangwu.shiyongjun import CurrentSpider as syjc
syjc()
#禽蛋
from new_agricultural.shangwu.qindan import CurrentSpider as qdc
qdc()
#肉类
from new_agricultural.shangwu.roulei import CurrentSpider as rlc
rlc()
#小麦
from new_agricultural.shangwu.xiaomai import CurrentSpider as xmc
xmc()
#玉米
from new_agricultural.shangwu.yumi import CurrentSpider as ymc
ymc()