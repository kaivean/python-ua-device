# -*- coding: utf8 -*-
import sys
import re
import os
import json
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('./')
from useragentBase import *

tmpData = {
    'ua': '',
    'match': None
}


def getMatch(string=None, reg=None, i=False):
    if not string:
        return tmpData['match']
    if i:
        tmpData['match'] = optimizedSearch(reg, string, re.I)
    else:
        tmpData['match'] = optimizedSearch(reg, string)
    return tmpData['match']


def parseUA(ua):
    tmpData['ua'] = ua
    uaData = UA(ua).getUaInfo()

    if not ua:
        return uaData

    # match = ''
    # tmpMatch = ''
    # handle mobile device
    if uaData['device']['type'] == 'mobile' or uaData['device']['type'] == 'tablet':

        # get manufacturer through the key words
        match = optimizedSearch(r'(ZTE|Samsung|Motorola|HTC|Coolpad|Huawei|Lenovo|LG|Sony Ericsson|Oppo|TCL|Vivo|Sony|Meizu|Nokia)', ua, re.I)
        if match:
            uaData['device']['manufacturer'] = match.group(1)
            if uaData['device']['model'] and match.group(1) in uaData['device']['model']:
                uaData['device']['model'] = uaData['device']['model'].replace(match.group(1), '')


        # handle Apple
        # 苹果就这3种iPod iPad iPhone
        if getMatch(ua, r'(iPod|iPad|iPhone)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Apple'
            uaData['device']['model'] = match.group(1)

        # handle Samsung
        # 特殊型号可能以xxx-开头 或者直接空格接型号 兼容build结尾或直接)结尾
        # Galaxy nexus才是三星 nexus是google手机
        # 三星手机类型：galaxy xxx|SM-xxx|GT-xxx|SCH-xxx|SGH-xxx|SPH-xxx|SHW-xxx  若这些均未匹配到，则启用在中关村在线爬取到的机型白名单进行判断
        elif getMatch(ua, r'[-\s](Galaxy[\s\-_]nexus|Galaxy[\s\-_]\w*[\s\-_]\w*|Galaxy[\s\-_]\w*|SM-\w*|GT-\w*|s[cgp]h-\w*|shw-\w*|ATIV|i9070|omnia|s7568|A3000|A3009|A5000|A5009|A7000|A7009|A8000|C101|C1116|C1158|E400|E500F|E7000|E7009|G3139D|G3502|G3502i|G3508|G3508J|G3508i|G3509|G3509i|G3558|G3559|G3568V|G3586V|G3589W|G3606|G3608|G3609|G3812|G388F|G5108|G5108Q|G5109|G5306W|G5308W|G5309W|G550|G600|G7106|G7108|G7108V|G7109|G7200|G720NO|G7508Q|G7509|G8508S|G8509V|G9006V|G9006W|G9008V|G9008W|G9009D|G9009W|G9198|G9200|G9208|G9209|G9250|G9280|I535|I679|I739|I8190N|I8262|I879|I879E|I889|I9000|I9060|I9082|I9082C|I9082i|I9100|I9100G|I9108|I9128|I9128E|I9128i|I9152|I9152P|I9158|I9158P|I9158V|I9168|I9168i|I9190|I9192|I9195|I9195I|I9200|I9208|I9220|I9228|I9260|I9268|I9300|I9300i|I9305|I9308|I9308i|I939|I939D|I939i|I9500|I9502|I9505|I9507V|I9508|I9508V|I959|J100|J110|J5008|J7008|N7100|N7102|N7105|N7108|N7108D|N719|N750|N7505|N7506V|N7508V|N7509V|N900|N9002|N9005|N9006|N9008|N9008S|N9008V|N9009|N9100|N9106W|N9108V|N9109W|N9150|N916|N9200|P709|P709E|P729|S6358|S7278|S7278U|S7562C|S7562i|S7898i|b9388)[\s\)]', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Samsung'
            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z]+[0-9]+[A-Z]*, 例如 G9006 G9006V 其实应该是G9006 另外三星只保留3位
            tmp = match.group(1)
            tmp = optimizedSub(r'Galaxy S VI', 'Galaxy S6', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S V', 'Galaxy S5', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S IV', 'Galaxy S4', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy s III', 'Galaxy S3', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S II', 'Galaxy S2', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S I', 'Galaxy S1', tmp, 1, re.I)
            uaData['device']['model'] = optimizedSub(r'([a-z]+[0-9]{3})[0-9]?[a-z]*', r'\1', tmp, 1, re.I)
            # match.group(1).replace(/Galaxy S VI/i, 'Galaxy S6')
            #     .replace(/Galaxy S V/i, 'Galaxy S5')
            #     .replace(/Galaxy S IV/i, 'Galaxy S4')
            #     .replace(/Galaxy s III/i, 'Galaxy S3')
            #     .replace(/Galaxy S II/i, 'Galaxy S2')
            #     .replace(/Galaxy S I/i, 'Galaxy S1')
            #     .replace(//i, '$1')

        # 针对三星已经匹配出的数据做处理
        elif uaData['device']['manufacturer'] and uaData['device']['manufacturer'].lower() == 'samsung' and uaData['device']['model']:
            tmp = uaData['device']['model']
            tmp = optimizedSub(r'Galaxy S VI', 'Galaxy S6', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S V', 'Galaxy S5', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S IV', 'Galaxy S4', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy s III', 'Galaxy S3', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S II', 'Galaxy S2', tmp, 1, re.I)
            tmp = optimizedSub(r'Galaxy S I', 'Galaxy S1', tmp, 1, re.I)
            uaData['device']['model'] = optimizedSub(r'([a-z]+[0-9]{3})[0-9]?[a-z]*', r'\1', tmp, 1, re.I)

            # uaData['device']['model'] = uaData['device']['model'].replace(/Galaxy S VI/i, 'Galaxy S6')
            #     .replace(/Galaxy S V/i, 'Galaxy S5')
            #     .replace(/Galaxy S IV/i, 'Galaxy S4')
            #     .replace(/Galaxy s III/i, 'Galaxy S3')
            #     .replace(/Galaxy S II/i, 'Galaxy S2')
            #     .replace(/Galaxy S I/i, 'Galaxy S1')
            #     .replace(/([a-z]+[0-9]{3})[0-9]?[a-z]*/i, '$1')

        # handle Huawei
        # 兼容build结尾或直接)结尾
        # 华为机型特征：Huawei[\s\-_](\w*[-_]?\w*)  或者以 7D-  ALE-  CHE-等开头
        elif getMatch(ua, r'(Huawei[\s\-_](\w*[-_]?\w*)|\s(7D-\w*|ALE-\w*|ATH-\w*|CHE-\w*|CHM-\w*|Che1-\w*|Che2-\w*|D2-\w*|G616-\w*|G620S-\w*|G621-\w*|G660-\w*|G750-\w*|GRA-\w*|Hol-\w*|MT2-\w*|MT7-\w*|PE-\w*|PLK-\w*|SC-\w*|SCL-\w*|H60-\w*|H30-\w*)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Huawei'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)

            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：xxx-[A-Z][0-9]+ 例如  H30-L01  H30-L00  H30-L20  都应该是 H30-L
            # h30-l  h30-h  h30-t 都是H30
            match = optimizedSearch(r'(\w*)[\s\-_]+[a-z0-9]+', uaData['device']['model'], re.I)
            if match:
                uaData['device']['model'] = match.group(1)


        # handle Xiaomi
        # 兼容build结尾或直接)结尾 以及特殊的HM处理方案(build/hm2013011)
        # xiaomi手机类型: mi m1 m2 m3 hm 开头
        # hongmi有特殊判断build/hm2015011
        elif getMatch(ua, r';\s(mi|m1|m2|m3|m4|hm)(\s*\w*)[\s\)]', True):
            match = getMatch()

            tmpMatch = optimizedSearch(r'(meitu|MediaPad)', ua, re.I)
            if tmpMatch:
                # 美图手机名字冒充小米 比如 meitu m4 mizhi
                uaData['device']['manufacturer'] = tmpMatch.group(1)
                uaData['device']['model'] = ''

            # 若匹配出的 match.group(2)没空格 会出现很多例如 mizi mizhi miha 但也会出现mi3 minote之类 特殊处理下
            elif len(match.group(2)) > 0 and not optimizedSearch(r'\s', match.group(2)):
                tmpMatch = optimizedSearch(r'(\d)', match.group(2), re.I)
                if tmpMatch:
                    uaData['device']['model'] = match.group(1) + '-' + tmpMatch.group(1)


            else:
                uaData['device']['manufacturer'] = 'Xiaomi'
                if match.group(2) and len(match.group(2)) > 0:
                    tmp = optimizedSub(r'\s', '', match.group(2), 1)
                    # tmp = match.group(2).replace(/\s/, '')
                    start = len(match.group(1)) - 2
                    uaData['device']['model'] = (match.group(1)[start:] + '-' + tmp)

                    uaData['device']['model'] = optimizedSub(r'm(\d)-', r'MI-\1', uaData['device']['model'], 1, re.I)
                    # uaData['device']['model'] = uaData['device']['model'].replace(//i, 'MI-$1')

                else:
                    start = len(match.group(1)) - 2
                    uaData['device']['model'] = match.group(1)[start:]
                    uaData['device']['model'] = optimizedSub(r'm(\d)', r'MI-\1', uaData['device']['model'], 1, re.I)

                # 解决移动联通等不同发行版导致的机型不同问题
                # 特征：mi-3c,例如mi-4LTE mi-4 其实应该是 mi-4
                if optimizedSearch(r'(mi|hm)(-\d)', uaData['device']['model'], re.I):
                    # 看看是不是 MI-3S  MI-4S....
                    match = optimizedSearch(r'(mi|hm)(-\ds)', uaData['device']['model'], re.I)
                    if match:
                        uaData['device']['model'] = match.group(1) + match.group(2)

                    # 防止 MI-20150XX等滥竽充数成为MI-2
                    elif getMatch(uaData['device']['model'], r'(mi|hm)(-\d{2})', True):
                        match = getMatch()
                        uaData['device']['model'] = match.group(1)

                    # 将mi-3c mi-3a mi-3w等合为mi-3
                    elif getMatch(uaData['device']['model'], r'(mi|hm)(-\d)[A-Z]', True):
                        match = getMatch()
                        uaData['device']['model'] = match.group(1) + match.group(2)


                # 去除 mi-4g这样的东西
                if getMatch(uaData['device']['model'], r'(mi|hm)(-\dg)', True):
                    match = getMatch()
                    uaData['device']['model'] = match.group(1)



        elif getMatch(ua, r'build\/HM\d{0,7}\)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Xiaomi'
            uaData['device']['model'] = 'HM'

        elif getMatch(ua, r'redmi\s?(\d+)?', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Xiaomi'
            # fix: Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 5 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.1 baiduboxapp/11.1.5.10 (Baidu; P1 8.1.0)
            # 比原有js多的逻辑，保证和js输出一致
            uaData['device']['model'] = 'HM-' + str(match.group(1) if match.group(1) else 'UNDEFINED')

        elif uaData['device']['manufacturer'] and uaData['device']['manufacturer'].lower() == 'xiaomi' and uaData['device']['model']:
            # 针对通过base库判断出数据时命名风格不同。特殊处理适配如下
            if getMatch(uaData['device']['model'], r'mi-one', True):
                uaData['device']['model'] = 'MI-1'

            # mi 2
            elif getMatch(uaData['device']['model'], r'mi-two', True):
                uaData['device']['model'] = 'MI-2'

            # 20150xxx2014501
            elif getMatch(uaData['device']['model'], r'\d{6}', True):
                uaData['device']['model'] = ''
            elif getMatch(uaData['device']['model'], r'redmi', True):
                uaData['device']['model'] = optimizedSub(r'redmi', r'HM', uaData['device']['model'].upper(), 1, re.I)
                # uaData['device']['model'] = uaData['device']['model'].upper().replace(/redmi/i, 'HM')

            # m1 m2 m3 写法不标准 另外判断是否是 m1-s
            elif getMatch(uaData['device']['model'], r'(m\d)[\s\-_](s?)', True):
                match = getMatch()
                uaData['device']['model'] = optimizedSub(r'm', r'MI-', match.group(1), 1, re.I) + match.group(2)
                # uaData['device']['model'] = match.group(1).replace(/m/, 'MI-') + match.group(2)

            # mi-2w  mi-3w 等格式化为mi-2  mi-3
            elif getMatch(uaData['device']['model'], r'(hm|mi)[\s\-_](\d?)[a-rt-z]', True):
                match = getMatch()
                tmpMatch = getMatch(uaData['device']['model'], r'(mi|hm)[\s\-_](note|pad)(\d?s?)', True)
                if tmpMatch:
                    uaData['device']['model'] = tmpMatch.group(1) + '-' + tmpMatch.group(2) + tmpMatch.group(3)

                else:
                    uaData['device']['model'] = (match.group(1) + '-' + match.group(2)) if match.group(2) else match.group(1)


            # 处理hm
            elif getMatch(uaData['device']['model'], r'hm', True):
                match = getMatch()
                # 判断是不是 hm-201xxx充数
                # if match = uaData['device']['model'].match(//i):
                if getMatch(uaData['device']['model'], r'(hm)[\s\-_](\d{2})', True):
                    match = getMatch()
                    uaData['device']['model'] = 'HM'

                # 判断是不是 hm-2s hm-1s
                # elif match = uaData['device']['model'].match(//i):
                elif getMatch(uaData['device']['model'], r'(hm)[\s\-_](\ds)', True):
                    match = getMatch()
                    uaData['device']['model'] = 'HM-' + match.group(2)

                # elif match = uaData['device']['model'].match(//i):
                elif getMatch(uaData['device']['model'], r'(hm)[\s\-_](\d)[a-z]', True):
                    match = getMatch()
                    uaData['device']['model'] = 'HM-' + match.group(2)

                else:
                    uaData['device']['model'] = 'HM'

                # 过滤类似 2g 3g等数据
                if optimizedSearch(r'hm-\dg', uaData['device']['model']):
                    uaData['device']['model'] = 'HM'



        # handle Vivo
        # 兼容build结尾或直接)结尾
        # vivo机型特征: Vivo[\s\-_](\w*)  或者以 E1  S11t  S7t 等开头
        # elif match = ua.match(//i):
        elif getMatch(ua, r'(vivo[\s\-_](\w*)|\s(E1\w?|E3\w?|E5\w?|V1\w?|V2\w?|S11\w?|S12\w?|S1\w?|S3\w?|S6\w?|S7\w?|S9\w?|X1\w?|X3\w?|X520\w?|X5\w?|X5Max|X5Max+|X5Pro|X5SL|X710F|X710L|Xplay|Xshot|Xpaly3S|Y11\w?|Y11i\w?|Y11i\w?|Y13\w?|Y15\w?|Y17\w?|Y18\w?|Y19\w?|Y1\w?|Y20\w?|Y22\w?|Y22i\w?|Y23\w?|Y27\w?|Y28\w?|Y29\w?|Y33\w?|Y37\w?|Y3\w?|Y613\w?|Y622\w?|Y627\w?|Y913\w?|Y923\w?|Y927\w?|Y928\w?|Y929\w?|Y937\w?)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Vivo'
            uaData['device']['model'] = match.group(1)
            # 首先剔除 viv-  vivo-  bbg- 等打头的内容
            uaData['device']['model'] = optimizedSub(r'(viv[\s\-_]|vivo[\s\-_]|bbg[\s\-_])', r'', uaData['device']['model'], 1, re.I)
            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z][0-9]+[A-Z] 例如  X5F X5L X5M X5iL 都应该是 X5
            if getMatch(uaData['device']['model'], r'([a-z]+[0-9]+)i?[a-z]?[\s\-_]?', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1)


        # handle Oppo
        # elif match = ua.match(//i):
        elif getMatch(ua, r'(Oppo[\s\-_](\w*)|\s(1100|1105|1107|3000|3005|3007|6607|A100|A103|A105|A105K|A109|A109K|A11|A113|A115|A115K|A121|A125|A127|A129|A201|A203|A209|A31|A31c|A31t|A31u|A51kc|A520|A613|A615|A617|E21W|Find|Mirror|N5110|N5117|N5207|N5209|R2010|R2017|R6007|R7005|R7007|R7c|R7t|R8000|R8007|R801|R805|R807|R809T|R8107|R8109|R811|R811W|R813T|R815T|R815W|R817|R819T|R8200|R8205|R8207|R821T|R823T|R827T|R830|R830S|R831S|R831T|R833T|R850|Real|T703|U2S|U521|U525|U529|U539|U701|U701T|U705T|U705W|X9000|X9007|X903|X905|X9070|X9077|X909|Z101|R829T)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Oppo'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)

            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z][0-9]+[A-Z] 例如  A31c A31s 都应该是 A31
            # 对 Plus 做特殊处理
            if getMatch(uaData['device']['model'], r'([a-z]+[0-9]+)-?(plus)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1) + '-' + match.group(2)

            elif getMatch(uaData['device']['model'], r'(\w*-?[a-z]+[0-9]+)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1)


        elif uaData['device']['manufacturer'] and uaData['device']['manufacturer'].lower() == 'oppo' and uaData['device']['model']:
            # 针对base库的数据做数据格式化处理
            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z][0-9]+[A-Z] 例如  A31c A31s 都应该是 A31
            # 对 Plus 做特殊处理
            # if match = uaData['device']['model'].match(//i):
            if getMatch(uaData['device']['model'], r'([a-z]+[0-9]+)-?(plus)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1) + '-' + match.group(2)

            elif getMatch(uaData['device']['model'], r'(\w*-?[a-z]+[0-9]+)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1)


        # handle Lenovo
        # 兼容build结尾或直接)结尾 兼容Lenovo-xxx/xxx以及Leveno xxx build等
        elif getMatch(ua, r'(Lenovo[\s\-_](\w*[-_]?\w*)|\s(A3580|A3860|A5500|A5600|A5860|A7600|A806|A800|A808T|A808T-I|A936|A938t|A788t|K30-E|K30-T|K30-W|K50-T3s|K50-T5|K80M|K910|K910e|K920|S90-e|S90-t|S90-u|S968T|X2-CU|X2-TO|Z90-3|Z90-7)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Lenovo'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)

            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z][0-9]+[A-Z] 例如  A360t A360 都应该是 A360
            if getMatch(uaData['device']['model'], r'([a-z]+[0-9]+)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1)


        # handle coolpad
        elif getMatch(ua, r'(Coolpad[\s\-_](\w*)|\s(7295C|7298A|7620L|8908|8085|8970L|9190L|Y80D)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Coolpad'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)


            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z][0-9]+[A-Z] 例如  8297-t01 8297-c01 8297w 都应该是 8297
            if getMatch(uaData['device']['model'], r'([a-z]?[0-9]+)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1)


        elif uaData['device']['manufacturer'] and uaData['device']['manufacturer'].lower() == 'coolpad' and uaData['device']['model']:
            # base 库适配
            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z][0-9]+[A-Z] 例如  8297-t01 8297-c01 8297w 都应该是 8297
            if getMatch(uaData['device']['model'], r'([a-z]?[0-9]+)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1)


        # handle meizu
        elif getMatch(ua, r'\s(mx\d*\w*|mz-(\w*))\s(\w*)\s*\w*\s*build', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Meizu'
            tmpModel = match.group(2) if match.group(2) else match.group(1)
            if match.group(3):
                uaData['device']['model'] = tmpModel + '-' + match.group(3)

            else:
                uaData['device']['model'] = tmpModel + ''


        elif getMatch(ua, r'(M463C|M35\d)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Meizu'
            uaData['device']['model'] = match.group(1)

        # handle htc
        elif getMatch(ua, r'(Htc[-_\s](\w*)|\s(601e|606w|608t|609d|610t|6160|619d|620G|626d|626s|626t|626w|709d|801e|802d|802t|802w|809D|816d|816e|816t|816v|816w|826d|826s|826t|826w|828w|901e|919d|A310e|A50AML|A510e|A620d|A620e|A620t|A810e|A9191|Aero|C620d|C620e|C620t|D316d|D516d|D516t|D516w|D820mt|D820mu|D820t|D820ts|D820u|D820us|E9pt|E9pw|E9sw|E9t|HD7S|M8Et|M8Sd|M8St|M8Sw|M8d|M8e|M8s|M8si|M8t|M8w|M9W|M9ew|Phablet|S510b|S510e|S610d|S710d|S710e|S720e|S720t|T327t|T328d|T328t|T328w|T329d|T329t|T329w|T528d|T528t|T528w|T8698|WF5w|X315e|X710e|X715e|X720d|X920e|Z560e|Z710e|Z710t|Z715e)[\s\)])', False):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Htc'
            uaData['device']['model'] = match.group(1)

        # handle Gionee
        elif getMatch(ua, r'(Gionee[\s\-_](\w*)|\s(GN\d+\w*)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Gionee'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)


        # handle LG
        elif getMatch(ua, r'(LG[-_](\w*)|\s(D728|D729|D802|D855|D856|D857|D858|D859|E985T|F100L|F460|H778|H818|H819|P895|VW820)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Lg'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)


        # handle tcl
        elif getMatch(ua, r'(Tcl[\s\-_](\w*)|\s(H916T|P588L|P618L|P620M|P728M)[\s\)])', False):
            match = getMatch()

            uaData['device']['manufacturer'] = 'Tcl'
            uaData['device']['model'] = match.group(1)

        # ZTE
        elif getMatch(ua, r'(V9180|N918)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Zte'
            uaData['device']['model'] = match.group(1)

        elif uaData['device']['manufacturer'] and uaData['device']['manufacturer'].lower() == 'zte' and uaData['device']['model']:
            # base 库适配
            # 解决移动联通等不同发行版导致的机型不同问题
            # 特征：[A-Z][0-9]+[A-Z] 例如  Q505T Q505u 都应该是 Q505
            if getMatch(uaData['device']['model'], r'([a-z]?[0-9]+)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1)


        # UIMI
        elif getMatch(ua, r'(UIMI\w*|umi\w*)[\s\-_](\w*)\s*\w*\s*build', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Uimi'
            if match.group(2):
                uaData['device']['model'] = match.group(1) + '-' + match.group(2)

            else:
                uaData['device']['model'] = match.group(1) + ''


        # eton
        elif getMatch(ua, r'eton[\s\-_](\w*)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Eton'
            uaData['device']['model'] = match.group(1)

        # Smartisan
        elif getMatch(ua, r'(SM705|SM701|YQ601|YQ603)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Smartisan'
            tmpMap = {
                'SM705': 'T1',
                'SM701': 'T1',
                'YQ601': 'U1',
                'YQ603': 'U1'
            }
            if match.group(1) in tmpMap:
                uaData['device']['model'] = tmpMap[match.group(1)]
            else:
                uaData['device']['model'] = match.group(1)
            # uaData['device']['model'] = ({
            #     SM705: 'T1',
            #     SM701: 'T1',
            #     YQ601: 'U1',
            #     YQ603: 'U1'
            # })[]or match.group(1)

        # handle Asus
        elif getMatch(ua, r'(Asus[\s\-_](\w*)|\s(A500CG|A500KL|A501CG|A600CG|PF400CG|PF500KL|T001|X002|X003|ZC500TG|ZE550ML|ZE551ML)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Asus'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)


        # handle nubia
        elif getMatch(ua, r'(Nubia[-_\s](\w*)|(NX501|NX505J|NX506J|NX507J|NX503A|nx\d+\w*)[\s\)])', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Nubia'
            if match.group(2):
                uaData['device']['model'] = match.group(2)

            elif match.group(3):
                uaData['device']['model'] = match.group(3)


        # handle haier
        elif getMatch(ua, r'(HT-\w*)|Haier[\s\-_](\w*-?\w*)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Haier'
            if match.group(1):
                uaData['device']['model'] = match.group(1)

            elif match.group(2):
                uaData['device']['model'] = match.group(2)


        # tianyu
        elif getMatch(ua, r'K-Touch[\s\-_](tou\s?ch\s?(\d)|\w*)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'K-Touch'
            if match.group(2):
                uaData['device']['model'] = 'Ktouch' + match.group(2)

            else:
                uaData['device']['model'] = match.group(1)



        # DOOV
        elif getMatch(ua, r'Doov[\s\-_](\w*)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Doov'
            uaData['device']['model'] = match.group(1)

        # coobee
        elif getMatch(ua, r'koobee', True):
            uaData['device']['manufacturer'] = 'koobee'


        # sony
        elif getMatch(ua, r'C69', True):
            uaData['device']['manufacturer'] = 'Sony'


        # haojixing
        elif getMatch(ua, r'N787|N818S', True):
            uaData['device']['manufacturer'] = 'Haojixing'


        # haisense
        elif getMatch(ua, r'(hs-|Hisense[\s\-_])(\w*)', True):
            match = getMatch()
            uaData['device']['manufacturer'] = 'Hisense'
            uaData['device']['model'] = match.group(2)

        #############################################################
        ###   格式化厂商
        ##########################################################

        # format the style of manufacturer
        if uaData['device']['manufacturer']:
            uaData['device']['manufacturer'] = uaData['device']['manufacturer'][0:1].upper() + uaData['device']['manufacturer'][1:].lower()

        # format the style of model
        if uaData['device']['model']:
            uaData['device']['model'] = optimizedSub(r'-+|_+|\s+', r' ', uaData['device']['model'].upper())
            uaData['device']['model'] = optimizedSearch(r'\s*(\w*\s*\w*)', uaData['device']['model']).group(1)
            uaData['device']['model'] = optimizedSub(r'\s+', r'-', uaData['device']['model'])

            # uaData['device']['model'] = uaData['device']['model'].upper().replace(//g, ' ')
            # uaData['device']['model'] = uaData['device']['model'].match(//)[1].replace(/\s+/, '-')

            # 针对三星、华为做去重的特殊处理
            if uaData['device']['manufacturer'] == 'Samsung':
                tmpMap = {
                    'SCH-I95': 'GT-I950',
                    'SCH-I93': 'GT-I930',
                    'SCH-I86': 'GT-I855',
                    'SCH-N71': 'GT-N710',
                    'SCH-I73': 'GT-S789',
                    'SCH-P70': 'GT-I915'
                }
                if uaData['device']['model'] in tmpMap:
                    uaData['device']['model'] = tmpMap[uaData['device']['model']]
                else:
                    uaData['device']['model'] = uaData['device']['model']

                # uaData['device']['model'] = ({
                #     'SCH-I95': 'GT-I950',
                #     'SCH-I93': 'GT-I930',
                #     'SCH-I86': 'GT-I855',
                #     'SCH-N71': 'GT-N710',
                #     'SCH-I73': 'GT-S789',
                #     'SCH-P70': 'GT-I915'
                # })[uaData['device']['model']]or uaData['device']['model']

            elif uaData['device']['manufacturer'] == 'Huawei':
                tmpMap = {
                    'CHE1': 'CHE',
                    'CHE2': 'CHE',
                    'G620S': 'G621',
                    'C8817D': 'G621'
                }
                if uaData['device']['model'] in tmpMap:
                    uaData['device']['model'] = tmpMap[uaData['device']['model']]
                else:
                    uaData['device']['model'] = uaData['device']['model']

                # uaData['device']['model'] = ({
                #     CHE1: 'CHE',
                #     CHE2: 'CHE',
                #     G620S: 'G621',
                #     C8817D: 'G621'
                # })[uaData['device']['model']]or uaData['device']['model']



        # 针对xiaomi 的部分数据没有格式化成功，格式化1次
        if uaData['device']['manufacturer'] and uaData['device']['manufacturer'] == 'Xiaomi':
            if getMatch(uaData['device']['model'], r'(hm|mi)-(note)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1) + '-' + match.group(2)

            elif getMatch(uaData['device']['model'], r'(hm|mi)-(\ds?)', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1) + '-' + match.group(2)

            elif getMatch(uaData['device']['model'], r'(hm|mi)-(\d)[a-rt-z]', True):
                match = getMatch()
                uaData['device']['model'] = match.group(1) + '-' + match.group(2)



    # handle browser
    # if (!uaData['browser']['name']) {
    # ua = ua.toLowerCase();
    if uaData['device']['type'] == 'desktop':

        # 360 security Explorer

        # if match = //i.exec(ua):
        if getMatch(ua, r'360se(?:[ \/]([\w.]+))?', True):
            match = getMatch()
            uaData['browser']['name'] = '360 security Explorer'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }


        # the world

        # elif match = //i.exec(ua):
        elif getMatch(ua, r'the world(?:[ \/]([\w.]+))?', True):
            match = getMatch()
            uaData['browser']['name'] = 'the world'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }


        # tencenttraveler

        # elif match = //i.exec(ua):
        elif getMatch(ua, r'tencenttraveler ([\w.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = 'tencenttraveler'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }


        # LBBROWSER

        # elif match = /LBBROWSER/i.exec(ua):
        elif getMatch(ua, r'LBBROWSER', True):
            match = getMatch()
            uaData['browser']['name'] = 'LBBROWSER'


    elif uaData['device']['type'] == 'mobile' or uaData['device']['type'] == 'tablet':

        # BaiduHD

        if getMatch(ua, r'BaiduHD\s+([\w.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = 'BaiduHD'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }


        # 360 Browser

        elif getMatch(ua, r'360.s*aphone\s*browser\s*\(version\s*([\w.]+)\)', True):
            match = getMatch()
            uaData['browser']['name'] = '360 Browser'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }


        # Baidu Browser

        # elif match = /flyflow\/([\w.]+)/i.exec(ua):
        elif getMatch(ua, r'flyflow\/([\w.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = 'Baidu Browser'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }



        # Baidu HD

        # elif match = /baiduhd ([\w.]+)/i.exec(ua):
        elif getMatch(ua, r'baiduhd ([\w.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = 'Baidu HD'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }



        # baidubrowser

        # elif match = //i.exec(ua):
        elif getMatch(ua, r'baidubrowser\/([\d\.]+)\s', True):
            match = getMatch()
            uaData['browser']['name'] = 'baidubrowser'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }



        # LieBaoFast

        # elif match = //i.exec(ua):
        elif getMatch(ua, r'LieBaoFast\/([\w.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = 'LieBao Fast'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }



        # LieBao

        # elif match = //i.exec(ua):
        elif getMatch(ua, r'LieBao\/([\w.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = 'LieBao'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }



        # SOUGOU

        # elif match = //i.exec(ua):
        elif getMatch(ua, r'Sogou\w+\/([0-9\.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = 'SogouMobileBrowser'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }



        # 百度国际

        # elif match = //i.exec(ua):
        elif getMatch(ua, r'bdbrowser\w+\/([0-9\.]+)', True):
            match = getMatch()
            uaData['browser']['name'] = '百度国际'
            uaData['browser']['version'] = {
                'original': match.group(1)
            }



        # Android Chrome Browser

        elif uaData['os']['name'] == 'Android' and optimizedSearch(r'safari', ua, re.I) and getMatch(ua, r'chrome\/([0-9\.]+)', True):
            match = getMatch()
            tmpMatch = getMatch(ua, r'\s+(\w+Browser)\/?([\d\.]*)')
            if tmpMatch:
                uaData['browser']['name'] = tmpMatch.group(1)
                if tmpMatch.group(2):
                    uaData['browser']['version'] = {'original': tmpMatch.group(2)}
                else:
                    uaData['browser']['version'] = {'original': match.group(1)}

            else:
                uaData['browser']['name'] = 'Android Chrome'
                uaData['browser']['version'] = {'original': match.group(1)}




        # Android Google Browser

        elif uaData['os']['name'] == 'Android' and optimizedSearch(r'safari', ua, re.I) and getMatch(ua, r'version\/([0-9\.]+)', True):
            match = getMatch()
            tmpMatch = getMatch(ua, r'\s+(\w+Browser)\/?([\d\.]*)')
            if tmpMatch:
                uaData['browser']['name'] = tmpMatch.group(1)
                if tmpMatch.group(2):
                    uaData['browser']['version'] = {'original': tmpMatch.group(2)}
                else:
                    uaData['browser']['version'] = {'original': match.group(1)}

            else:
                uaData['browser']['name'] = 'Android Browser'
                uaData['browser']['version'] = {'original': match.group(1)}




        # 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B206' belongs to Safari

        elif getMatch(ua, r'(ipad|iphone).* applewebkit\/.* mobile', True):
            match = getMatch()
            uaData['browser']['name'] = 'Safari'


    if getMatch(ua, r'baiduboxapp\/?([\d\.]*)', True):
        match = getMatch()
        uaData['browser']['name'] = '百度框'
        if match.group(1):
            uaData['browser']['version'] = {
                'original': match.group(1)
            }

        # uaData['browser']['name'] = 'baidu box';

    elif getMatch(ua, r'BaiduLightAppRuntime', True):
        match = getMatch()
        uaData['browser']['name'] = '轻应用runtime'
        # uaData['browser']['name'] = 'qing runtime';

    elif getMatch(ua, r'Weibo', True):
        match = getMatch()
        uaData['browser']['name'] = '微博'
        # uaData['browser']['name'] = 'weibo';

    elif getMatch(ua, r'MQQ', True):
        match = getMatch()
        uaData['browser']['name'] = '手机QQ'
        # uaData['browser']['name'] = 'mobile qq';

    elif getMatch(ua, r'hao123', True):
        match = getMatch()
        uaData['browser']['name'] = 'hao123'

    # }
    if getMatch(ua, r'MicroMessenger\/([\w.]+)', True):
        match = getMatch()
        uaData['browser']['name'] = '微信'
        # optimizedSub(r'-+|_+|\s+', r' ', )
        tmpVersion = match.group(1).replace('_', '.')
        tmpMatch = getMatch(tmpVersion, r'(\d+\.\d+\.\d+\.\d+)')
        # tmpMatch = //.exec(tmpVersion)
        if tmpMatch:
            tmpVersion = tmpMatch.group(1)

        uaData['browser']['version'] = {
            'original': tmpVersion
        }

    elif getMatch(ua, r'UCBrowser\/([\w.]+)', True):
        match = getMatch()
        uaData['browser']['name'] = 'UC Browser'
        uaData['browser']['version'] = {
            'original': match.group(1)
        }

    if getMatch(ua, r'OPR\/([\w.]+)', True):
        match = getMatch()
        uaData['browser']['name'] = 'Opera'
        uaData['browser']['version'] = {
            'original': match.group(1)
        }
    elif getMatch(ua, r'OPiOS\/([\w.]+)', True):
        match = getMatch()
        uaData['browser']['name'] = 'Opera'
        uaData['browser']['version'] = {
            'original': match.group(1)
        }

    # IE 11
    # elif //i.test(ua) and //i.test(ua):
    elif getMatch(ua, r'Trident\/7', True) and getMatch(ua, r'rv:11', True):
        uaData['browser']['name'] = 'Internet Explorer'
        uaData['browser']['version'] = {
            'major': '11',
            'original': '11'
        }

    # Microsoft Edge
    elif getMatch(ua, r'Edge\/12', True) and getMatch(ua, r'Windows Phone|Windows NT', True):
        uaData['browser']['name'] = 'Microsoft Edge'
        uaData['browser']['version'] = {
            'major': '12',
            'original': '12'
        }

    # miui browser
    # elif match = //i.exec(ua):
    elif getMatch(ua, r'miuibrowser\/([\w.]+)', True):
        match = getMatch()
        uaData['browser']['name'] = 'miui browser'
        uaData['browser']['version'] = {
            'original': match.group(1)
        }

    # Safari
    if not uaData['browser']['name']:
        if getMatch(ua, r'Safari\/([\w.]+)', True) and optimizedSearch(r'Version', ua, re.I):
            match = getMatch()
            uaData['browser']['name'] = 'Safari'


    if uaData['browser']['name'] and not uaData['browser']['version']['original']:
        # if match = //i.exec(ua):
        if getMatch(ua, r'Version\/([\w.]+)', True):
            match = getMatch()
            uaData['browser']['version'] =  {
                'original': match.group(1)
            }



    # if (uaData['os']['name'] === 'Windows' && uaData['os']['version']) {
    #  // Windows 8.1
    #  if (uaData['os']['version'].alias === 'NT 6.3') {
    #      uaData['os']['version'].alias = '8.1';
    #  }
    # }
    # handle os
    if uaData['os']['name'] == 'Windows'or optimizedSearch(r'Windows', ua, re.I):
        uaData['os']['name'] = 'Windows'
        if optimizedSearch(r'NT 6.3', ua, re.I):
            uaData['os']['version'] = {
                'alias': '8.1',
                'original': '8.1'
            }

        elif optimizedSearch(r'NT 6.4', ua, re.I) or optimizedSearch(r'NT 10.0', ua, re.I):
            uaData['os']['version'] = {
                'alias': '10',
                'original': '10'
            }


    elif uaData['os']['name'] == 'Mac OS X':
        uaData['os']['name'] = 'Mac OS X'
        if getMatch(ua, r'Mac OS X[\s\_\-\/](\d+[\.\-\_]\d+[\.\-\_]?\d*)', True):
            match = getMatch()
            uaData['os']['version'] = {
                'alias': match.group(1).replace('_', '.'),
                'original': match.group(1).replace('_', '.')
            }

        else:
            uaData['os']['version'] = {
                'alias': '',
                'original': ''
            }


    elif optimizedSearch(r'Android', uaData['os']['name'], re.I):
        if getMatch(ua, r'Android[\s\_\-\/i686]?[\s\_\-\/](\d+[\.\-\_]\d+[\.\-\_]?\d*)', True):
            match = getMatch()
            uaData['os']['version'] = {
                'alias': match.group(1),
                'original': match.group(1)
            }


    return uaData



