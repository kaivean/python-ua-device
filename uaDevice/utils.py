import re

# 正则表达式缓存
regObj = {}

def optimizedSearch(regStr, matchStr, flags=0):
    """
    优化的正则搜索函数
    regStr: 正则表达式字符串
    matchStr: 要匹配的字符串
    flags: 正则标志
    """
    if regStr not in regObj:
        regObj[regStr] = re.compile(regStr, flags)
    return regObj[regStr].search(matchStr)

def optimizedSub(regStr, replaceStr, matchStr, count=0, flags=0):
    """
    优化的正则替换函数
    regStr: 正则表达式字符串
    replaceStr: 替换字符串
    matchStr: 要匹配的字符串
    count: 替换次数
    flags: 正则标志
    """
    if regStr not in regObj:
        regObj[regStr] = re.compile(regStr, flags)
    return regObj[regStr].sub(replaceStr, matchStr, count=count)

# 匹配结果缓存
tmpData = {
    'ua': '',
    'match': None
}

def getMatch(string=None, reg=None, i=False):
    """
    获取正则匹配结果
    string: 要匹配的字符串
    reg: 正则表达式
    i: 是否忽略大小写
    """
    if string is None:
        return tmpData['match']
    flags = re.I if i else 0
    tmpData['match'] = optimizedSearch(reg, string, flags)
    return tmpData['match'] is not None

def cleanupModel(s=''):
    """
    清理设备型号字符串
    s: 设备型号字符串
    """
    if not s:
        return s

    # 基本清理
    s = optimizedSub(r'_TD$|_CMCC$', '', s, 1)
    s = optimizedSub(r'_', ' ', s)
    s = optimizedSub(r'^\s+|\s+$', '', s)
    s = optimizedSub(r'\/[^/]+$|\/[^/]+ Android\/.*', '', s, 1)

    # 移除常见前缀
    s = optimizedSub(r'^(Android on |Android for |ICS AOSP on )', '', s, 1)

    # 处理品牌前缀
    s = optimizedSub(r'^Huawei[ -]', 'Huawei ', s, 1, re.I)
    s = optimizedSub(r'^SAMSUNG[ -]', '', s, 1, re.I)
    s = optimizedSub(r'^Lenovo[ -]', 'Lenovo ', s, 1)
    s = optimizedSub(r'^(LG)[ _\/]', r'\1-', s, 1)
    s = optimizedSub(r'^(HTC)[-\/]', r'\1 ', s, 1)
    s = optimizedSub(r'^(Motorola[\s|-]|Moto|MOT-)', '', s, 1)

    # 移除运营商和URL
    s = optimizedSub(r'-?(orange(-ls)?|vodafone|bouygues)$', '', s, 1, re.I)
    s = optimizedSub(r'http:\/\/.+$', '', s, 1, re.I)

    return s.strip()