# -*- coding: utf8 -*-
import sys
import re
import os
import time
import json
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('uaDevice')
import uaDevice

if __name__ == '__main__':
    f = open('test/data10000.txt')
    # f = open('test1/data10000.2.txt')
    data = f.read()

    uas = data.split('\n')

    stat = {
        'osName': [0, [], []],
        'osVersion': [0, [], []],
        'browserName': [0, [], []],
        'browserVersion': [0, [], []],
        'engineName': [0, [], []],
        'engineVersion': [0, [], []],
        'deviceType': [0, [], []],
        'deviceModel': [0, [], []],
        'deviceManufacturer': [0, [], []]
    }
    total = len(uas)
    start = time.time() * 1000
    for i in range(total):
        ua = uas[i]

        # if i + 1 != 1955:
        #     continue
        # print 'ua: ', ua, len(ua)

        s = time.time() * 1000
        info = uaDevice.parseUA(ua)
        output = '\t'.join([
            info['os']['name'],
            info['os']['version']['original'],
            info['browser']['name'],
            info['browser']['version']['original'],
            info['engine']['name'],
            info['engine']['version']['original'],
            info['device']['type'],
            info['device']['model'],
            info['device']['manufacturer']
        ])
        print(output)

        stat['osName'][2].append(info['os']['name'])
        if not info['os']['name']:
            stat['osName'][0] += 1
            stat['osName'][1].append(info['os']['name'])

        stat['osVersion'][2].append(info['os']['version']['original'])
        if not info['os']['version']['original']:
            stat['osVersion'][0] += 1
            stat['osVersion'][1].append(info['os']['version']['original'])

        stat['browserName'][2].append(info['browser']['name'])
        if not info['browser']['name']:
            stat['browserName'][0] += 1
            stat['browserName'][1].append(info['browser']['name'])

        stat['browserVersion'][2].append(info['browser']['version']['original'])
        if not info['browser']['version']['original']:
            stat['browserVersion'][0] += 1
            stat['browserVersion'][1].append(info['browser']['version']['original'])

        stat['engineName'][2].append(info['engine']['name'])
        if not info['engine']['name']:
            stat['engineName'][0] += 1
            stat['engineName'][1].append(info['engine']['name'])

        stat['engineVersion'][2].append(info['engine']['version']['original'])
        if not info['engine']['version']['original']:
            stat['engineVersion'][0] += 1
            stat['engineVersion'][1].append(info['engine']['version']['original'])

        stat['deviceType'][2].append(info['device']['type'])
        if not info['device']['type']:
            stat['deviceType'][0] += 1
            stat['deviceType'][1].append(info['device']['type'])

        stat['deviceModel'][2].append(info['device']['model'])
        if not info['device']['model']:
            stat['deviceModel'][0] += 1
            stat['deviceModel'][1].append(info['device']['model'])

        stat['deviceManufacturer'][2].append(info['device']['manufacturer'])
        if not info['device']['manufacturer']:
            stat['deviceManufacturer'][0] += 1
            stat['deviceManufacturer'][1].append(info['device']['manufacturer'])


    for key in stat.keys():
        print >> sys.stderr, "%s: 成功数:%s， 成功率: %s%%" % (key, str(total - stat[key][0]), str(float(total - stat[key][0])/total*100))

    # for key in stat.keys():
    #     print >> sys.stderr, key, json.dumps(list(set(stat[key][2])))

    print >> sys.stderr, 'Total ua number: ', total,  ' Total time', i, time.time() * 1000  - start, 'ms'
