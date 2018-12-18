# -*- coding: utf8 -*-
import sys
import re
import os
import json
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('./')

from regs import *
from models import *

regObj = {

}

def optimizedSearch(regStr, matchStr, flags=0):
    if regStr not in regObj:
        regObj[regStr] = re.compile(regStr, flags)

    return regObj[regStr].search(matchStr)


def optimizedSub(regStr, replaceStr, matchStr, count=0, flags=0):
    if regStr not in regObj:
        regObj[regStr] = re.compile(regStr, flags)

    return regObj[regStr].sub(replaceStr, matchStr, count=count)


class Version(object):
    def __init__(self, v={}):
        """
        初始化
        """
        self.original = v['value'] if 'value' in v else ''
        self.alias = v['alias'] if 'alias' in v else ''
        self.details = v['details'] if 'details' in v else None
        self.minor = -1
        self.type = ''


class UA(object):
    def __init__(self, ua, options=None):
        """
        初始化
        """

        self.options = {
            'useFeatures': options['useFeatures'] if options else False,
            'detectCamouflage': options['detectCamouflage'] if options else True
        }

        self.browser = {
            'name': '',
            'version': Version(),
            'mode': '', # desktop mobile
            'details': 0,
            'stock': True,
            'hidden': False,
            'channel': ''
        }
        self.engine = {
            'name': '',  # Webkit Presto
            'version': Version()
        }
        self.os = {
            'name': '',
            'version': Version()
        }
        self.device = {
            'type': 'desktop',
            'identified': False,
            'manufacturer': '',
            'model': '',
        }

        self.camouflage = False
        self.features = []
        if ua:
            self.detect(ua)


    def getUaInfo(self):
        return {
            'os': {
                'name': self.os['name'],
                'version': {
                    'alias': self.os['version'].alias if self.os['version'] else '',
                    'original': self.os['version'].original if self.os['version'] else '',
                }
            },
            'browser': {
                'name': self.browser['name'],
                'mode': self.browser['mode'],
                'version': {
                    'alias': self.browser['version'].alias if self.browser['version'] else '',
                    'original': self.browser['version'].original if self.browser['version'] else '',
                }
            },
            'engine': {
                'name': self.engine['name'],
                'version': {
                    'alias': self.engine['version'].alias,
                    'original': self.engine['version'].original
                }
            },
            'device': {
                'type': self.device['type'],
                'manufacturer': self.device['manufacturer'],
                'model': self.device['model']
            }
        }

    def detect(self, ua):


        # Unix
        #

        if 'Unix' in ua:
            self.os['name'] = 'Unix'



        # FreeBSD
        #

        if 'FreeBSD' in ua:
            self.os['name'] = 'FreeBSD'



        # OpenBSD
        #

        if 'OpenBSD' in ua:
            self.os['name'] = 'OpenBSD'



        # NetBSD
        #

        if 'NetBSD' in ua:
            self.os['name'] = 'NetBSD'



        # SunOS
        #

        if 'SunOS' in ua:
            self.os['name'] = 'Solaris'



        # Linux
        #

        if 'Linux' in ua:
            self.os['name'] = 'Linux'

            if 'CentOS' in ua:
                self.os['name'] = 'CentOS'
                match = optimizedSearch(r'CentOS\/[0-9\.\-]+el([0-9_]+)', ua)
                if match:
                    self.os['version'] = Version({
                        'value': match.group(1).replace('_', '.')
                    })



            if 'Debian' in ua:
                self.os['name'] = 'Debian'


            if 'Fedora' in ua:
                self.os['name'] = 'Fedora'
                match = optimizedSearch(r'Fedora\/[0-9\.\-]+fc([0-9]+)', ua)
                if match:
                    self.os['version'] = Version({
                        'value': match.group(1)
                    })



            if 'Gentoo' in ua:
                self.os['name'] = 'Gentoo'


            if 'Kubuntu' in ua:
                self.os['name'] = 'Kubuntu'


            if 'Mandriva Linux' in ua:
                self.os['name'] = 'Mandriva'
                match = optimizedSearch(r'Mandriva Linux\/[0-9\.\-]+mdv([0-9]+)', ua)
                if match:
                    self.os['version'] = Version({
                        'value': match.group(1)
                    })



            if 'Mageia' in ua:
                self.os['name'] = 'Mageia'
                match = optimizedSearch(r'Mageia\/[0-9\.\-]+mga([0-9]+)', ua)
                if match:
                    self.os['version'] = Version({
                        'value': match.group(1)
                    })



            if 'Red Hat' in ua:
                self.os['name'] = 'Red Hat'
                match = optimizedSearch(r'Red Hat[^\/]*\/[0-9\.\-]+el([0-9_]+)', ua)
                if match:
                    self.os['version'] = Version({
                        'value': match.group(1).replace('_', '.')
                    })



            if 'Slackware' in ua:
                self.os['name'] = 'Slackware'


            if 'SUSE' in ua:
                self.os['name'] = 'SUSE'


            if 'Turbolinux' in ua:
                self.os['name'] = 'Turbolinux'


            if 'Ubuntu' in ua:
                self.os['name'] = 'Ubuntu'
                match = optimizedSearch(r'Ubuntu\/([0-9.]*)', ua)
                if match:
                    self.os['version'] = Version({
                        'value': match.group(1)
                    })





        # iOS
        #
        if optimizedSearch(r'iPhone( Simulator)?;', ua) or 'iPad;' in ua or 'iPod;' in ua or optimizedSearch(r'iPhone\s*\d*s?[cp]?;', ua, re.I):
            self.os['name'] = 'iOS'
            self.os['version'] = Version({
                'value': '1.0'
            })
            # fix: 懒匹配，不然会包含like等
            match = optimizedSearch(r'OS (.*?) like Mac OS X', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1).replace('_', '.')
                })


            if 'iPhone Simulator;' in ua:
                self.device['type'] = 'emulator'
            elif 'iPod;' in ua:
                self.device['type'] = 'media'
                self.device['manufacturer'] = 'Apple'
                self.device['model'] = 'iPod Touch'
            elif 'iPhone;' in ua or optimizedSearch(r'iPhone\s*\d*s?[cp]?;', ua, re.I):
                self.device['type'] = 'mobile'
                self.device['manufacturer'] = 'Apple'
                self.device['model'] = 'iPhone'
            else:
                self.device['type'] = 'tablet'
                self.device['manufacturer'] = 'Apple'
                self.device['model'] = 'iPad'


            self.device['identified'] = True



        # MacOS X
        #

        elif 'Mac OS X' in ua:
            self.os['name'] = 'Mac OS X'
            match = optimizedSearch(r'Mac OS X (10[0-9\._]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1).replace('_', '.')
                })




        # Windows
        #

        if 'Windows' in ua:
            self.os['name'] = 'Windows'
            match = optimizedSearch(r'Windows NT ([0-9]\.[0-9])', ua)
            if match:
                self.os['version'] = parseVersion(match.group(1))
                tmpMap = {
                    '6.2': '8',
                    '6.1': '7',
                    '6.0': 'Vista',
                    '5.2': 'Server 2003',
                    '5.1': 'XP',
                    '5.0': '2000'
                }
                if match.group(1) in tmpMap:
                    self.os['version'] = Version({
                        'value': match.group(1),
                        'alias': tmpMap[match.group(1)]
                    })
                else:
                    self.os['version'] = Version({
                        'value': match.group(1),
                        'alias': 'NT ' + str(self.os['version'])
                    })



            if 'Windows 95' in ua or 'Win95' in ua or 'Win 9x 4.00' in ua:
                self.os['version'] = Version({
                    'value': '4.0',
                    'alias': '95'
                })


            if 'Windows 98' in ua or 'Win98' in ua or 'Win 9x 4.10' in ua:
                self.os['version'] = Version({
                    'value': '4.1',
                    'alias': '98'
                })


            if 'Windows ME' in ua or 'WinME' in ua or 'Win 9x 4.90' in ua:
                self.os['version'] = Version({
                    'value': '4.9',
                    'alias': 'ME'
                })


            if 'Windows XP' in ua or 'WinXP' in ua:
                self.os['name'] = Version({
                    'value': '5.1',
                    'alias': 'XP'
                })


            if 'WP7' in ua:
                self.os['name'] = 'Windows Phone'
                self.os['version'] = Version({
                    'value': '7.0',
                    'details': 2
                })
                self.device['type'] = 'mobile'
                self.browser['mode'] = 'desktop'


            if 'Windows CE' in ua or 'WinCE' in ua or 'WindowsCE' in ua:
                if ' IEMobile' in ua:
                    self.os['name'] = 'Windows Mobile'

                    if ' IEMobile 8' in ua:
                        self.os['version'] = Version({
                            'value': '6.5',
                            'details': 2
                        })


                    if ' IEMobile 7' in ua:
                        self.os['version'] = Version({
                            'value': '6.1',
                            'details': 2
                        })


                    if ' IEMobile 6' in ua:
                        self.os['version'] = Version({
                            'value': '6.0',
                            'details': 2
                        })

                else:
                    self.os['name'] = 'Windows CE'
                    match = optimizedSearch(r'WindowsCEOS\/([0-9.]*)', ua)
                    if match:
                        self.os['version'] = Version({
                            'value': match.group(1),
                            'details': 2
                        })

                    match = optimizedSearch(r'Windows CE ([0-9.]*)', ua)
                    if match:
                        self.os['version'] = Version({
                            'value': match.group(1),
                            'details': 2
                        })



                self.device['type'] = 'mobile'


            if 'Windows Mobile' in ua:
                self.os['name'] = 'Windows Mobile'
                self.device['type'] = 'mobile'

            match = optimizedSearch(r'WindowsMobile\/([0-9.]*)', ua)
            if match:
                self.os['name'] = 'Windows Mobile'
                self.os['version'] = Version({
                    'value': match.group(1),
                    'details': 2
                })
                self.device['type'] = 'mobile'

            match = optimizedSearch(r'Windows Phone [0-9]', ua)
            if match:
                self.os['name'] = 'Windows Mobile'
                self.os['version'] = Version({
                    'value': optimizedSearch(r'Windows Phone ([0-9.]*)', ua).group(1),
                    'details': 2
                })
                self.device['type'] = 'mobile'


            if 'Windows Phone OS' in ua:
                self.os['name'] = 'Windows Phone'

                # fix
                ver = optimizedSearch(r'Windows Phone OS ([0-9.]*)', ua).group(1)
                self.os['version'] = Version({
                    'value': ver,
                    'details': 2
                })
                ver = ver or '0'
                ver = float('.'.join(ver.split('.')[:2])) # 取两位
                if ver < 7:
                    self.os['name'] = 'Windows Mobile'

                match = optimizedSearch(r'IEMobile\/[^;]+; ([^;]+); ([^;]+)[;|\)]', ua)
                if match:
                    self.device['manufacturer'] = match.group(1)
                    self.device['model'] = match.group(2)


                self.device['type'] = 'mobile'

                manufacturer = self.device['manufacturer']
                model = cleanupModel(self.device['model'])

                if manufacturer in WINDOWS_PHONE_MODELS and model in WINDOWS_PHONE_MODELS[manufacturer]:
                    self.device['manufacturer'] = WINDOWS_PHONE_MODELS[manufacturer][model][0]
                    self.device['model'] = WINDOWS_PHONE_MODELS[manufacturer][model][1]
                    self.device['identified'] = True


                if manufacturer is 'Microsoft' and model is 'XDeviceEmulator':
                    self.device['manufacturer'] = None
                    self.device['model'] = None
                    self.device['type'] = 'emulator'
                    self.device['identified'] = True





        # Android
        #
        if 'Android' in ua:
            self.os['name'] = 'Android'
            self.os['version'] = None

            match = optimizedSearch(r'Android(?: )?(?:AllPhone_|CyanogenMod_)?(?:\/)?v?([0-9.]+)', ua.replace('-update', '.'))
            if match:
                self.os['version'] = Version({
                    'value': match.group(1),
                    'details': 3
                })


            if 'Android Eclair' in ua:
                self.os['version'] = Version({
                    'value': '2.0',
                    'details': 3
                })


            self.device['type'] = 'mobile'

            # fix: 原js里，可能是个bug，version不是数字，是对象
            if self.os['version']:
                ver = self.os['version'].original or '0'
                ver = float('.'.join(ver.split('.')[:2])) # 取两位
                if self.os['version'].original >= 3:
                    self.device['type'] = 'tablet'
                if self.os['version'].original >= 4 and 'Mobile' in ua:
                    self.device['type'] = 'mobile'

                # 比原js多的逻辑
                if 'ZTEQ801' in ua:
                    self.device['type'] = 'mobile'


            tmpArr = [
                'Eclair; (?:[a-zA-Z][a-zA-Z](?:[-_][a-zA-Z][a-zA-Z])?) Build\/([^\/]*)\/',
                '; ([^;]*[^;\s])\s+Build',
                '[a-zA-Z][a-zA-Z](?:[-_][a-zA-Z][a-zA-Z])?; ([^;]*[^;\s]);\s+Build',
                '\(([^;]+);U;Android\/[^;]+;[0-9]+\*[0-9]+;CTC\/2.0\)',
                ';\s?([^;]+);\s?[0-9]+\*[0-9]+;\s?CTC\/2.0',
                'zh-cn;\s*(.*?)(\/|build)',
                'Android [^;]+; (?:[a-zA-Z][a-zA-Z](?:[-_][a-zA-Z][a-zA-Z])?; )?([^)]+)\)',
                '^(.+?)\/\S+'
            ]
            for regstr in tmpArr:
                if regstr ==  tmpArr[-1]:
                    match = optimizedSearch(regstr, ua, re.I)
                else:
                    match = optimizedSearch(regstr, ua)

                if match:
                    if regstr == tmpArr[-2]:
                        if not optimizedSearch(r'[a-zA-Z][a-zA-Z](?:[-_][a-zA-Z][a-zA-Z])?', ua):
                            self.device['model'] = match.group(1)
                    else:
                        self.device['model'] = match.group(1)
                    break
            # origin
            # if match:

            # elif match = //.exec(ua):
            #     self.device['model'] = match.group(1)
            # elif match = //.exec(ua):
            #     self.device['model'] = match.group(1)
            # elif match = //.exec(ua):
            #     self.device['model'] = match.group(1)
            # elif match = //.exec(ua):
            #     self.device['model'] = match.group(1)
            # elif match = //i.exec(ua):
            #     self.device['model'] = match.group(1)
            # elif match = //.exec(ua):
            #     if not ua.match(/[a-zA-Z][a-zA-Z](?:[-_][a-zA-Z][a-zA-Z])?/):
            #         self.device['model'] = match.group(1)

            # elif match = /^(.+?)\/\S+/i.exec(ua):
            #     self.device['model'] = match.group(1)



            """Sometimes we get a model name that starts with Android, in that case it is a mismatch and we should ignore it"""
            if self.device['model'] and self.device['model'][0:7] is 'Android':
                self.device['model'] = None


            if self.device['model']:
                model = cleanupModel(self.device['model'])

                if model in ANDROID_MODELS:
                    self.device['manufacturer'] = ANDROID_MODELS[model][0]
                    self.device['model'] = ANDROID_MODELS[model][1]
                    if len(ANDROID_MODELS[model]) > 2:
                        self.device['type'] = ANDROID_MODELS[model][2]
                    self.device['identified'] = True


                if model == 'Emulator ' or model == 'x86 Emulator' or model == 'x86 VirtualBox' or model == 'vm':
                    self.device['manufacturer'] = None
                    self.device['model'] = None
                    self.device['type'] = 'emulator'
                    self.device['identified'] = True



            if 'HP eStation' in ua:
                self.device['manufacturer'] = 'HP'
                self.device['model'] = 'eStation'
                self.device['type'] = 'tablet'
                self.device['identified'] = True

            match = optimizedSearch(r'Pre\/1.0', ua)
            if match:
                self.device['manufacturer'] = 'Palm'
                self.device['model'] = 'Pre'
                self.device['identified'] = True

            match = optimizedSearch(r'Pre\/1.1', ua)
            if match:
                self.device['manufacturer'] = 'Palm'
                self.device['model'] = 'Pre Plus'
                self.device['identified'] = True

            match = optimizedSearch(r'Pre\/1.2', ua)
            if match:
                self.device['manufacturer'] = 'Palm'
                self.device['model'] = 'Pre 2'
                self.device['identified'] = True

            match = optimizedSearch(r'Pre\/3.0', ua)
            if match:
                self.device['manufacturer'] = 'HP'
                self.device['model'] = 'Pre 3'
                self.device['identified'] = True

            match = optimizedSearch(r'Pixi\/1.0', ua)
            if match:
                self.device['manufacturer'] = 'Palm'
                self.device['model'] = 'Pixi'
                self.device['identified'] = True

            match = optimizedSearch(r'Pixi\/1.1', ua)
            if match:
                self.device['manufacturer'] = 'Palm'
                self.device['model'] = 'Pixi Plus'
                self.device['identified'] = True

            match = optimizedSearch(r'P160UN?A?\/1.0', ua)
            if match:
                self.device['manufacturer'] = 'HP'
                self.device['model'] = 'Veer'
                self.device['identified'] = True




        # Google TV
        #

        if 'GoogleTV' in ua:
            self.os['name'] = 'Google TV'
            match = optimizedSearch(r'Chrome/5.', ua)
            if match:
                self.os['version'] = Version({
                    'value': '1'
                })

            match = optimizedSearch(r'Chrome/11.', ua)
            if match:
                self.os['version'] = Version({
                    'value': '2'
                })


            self.device['type'] = 'television'



        # WoPhone
        #

        if 'WoPhone' in ua:
            self.os['name'] = 'WoPhone'
            match = optimizedSearch(r'WoPhone\/([0-9\.]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })


            self.device['type'] = 'mobile'



        # BlackBerry
        #

        if 'BlackBerry' in ua:
            self.os['name'] = 'BlackBerry OS'

            if 'Opera' not in ua:
                match = optimizedSearch(r'BlackBerry([0-9]*)\/([0-9.]*)', ua)
                if match:
                    self.device['model'] = match.group(1)
                    self.os['version'] = Version({
                        'value': match.group(2),
                        'details': 2
                    })

                match = optimizedSearch(r'; BlackBerry ([0-9]*);', ua)
                if match:
                    self.device['model'] = match.group(1)

                match = optimizedSearch(r'Version\/([0-9.]*)', ua)
                if match:
                    self.os['version'] = Version({
                        'value': match.group(1),
                        'details': 2
                    })

                # fix
                ver = '0'
                if self.os['version']:
                    ver = self.os['version'].original
                ver = float('.'.join(ver.split('.')[:2])) # 只要一个dot，否则float报错
                if ver >= 10:
                    self.os['name'] = 'BlackBerry'


                if self.device['model']:
                    if self.device['model'] in BLACKBERRY_MODELS:
                        self.device['model'] = 'BlackBerry ' + BLACKBERRY_MODELS[self.device['model']] + ' ' + self.device['model']
                    else:
                        self.device['model'] = 'BlackBerry ' + self.device['model']

                else:
                    self.device['model'] = 'BlackBerry'

            else:
                self.device['model'] = 'BlackBerry'


            self.device['manufacturer'] = 'RIM'
            self.device['type'] = 'mobile'
            self.device['identified'] = True



        # BlackBerry PlayBook
        #

        if 'RIM Tablet OS' in ua:
            self.os['name'] = 'BlackBerry Tablet OS'

            self.os['version'] = Version({
                'value': optimizedSearch(r'RIM Tablet OS ([0-9.]*)', ua).groups(1),
                'details': 2
            })

            self.device['manufacturer'] = 'RIM'
            self.device['model'] = 'BlackBerry PlayBook'
            self.device['type'] = 'tablet'
            self.device['identified'] = True
        elif 'PlayBook' in ua:
            match = optimizedSearch(r'Version\/(10[0-9.]*)', ua)
            if match:
                self.os['name'] = 'BlackBerry'
                self.os['version'] = Version({
                    'value': match.group(1),
                    'details': 2
                })

                self.device['manufacturer'] = 'RIM'
                self.device['model'] = 'BlackBerry PlayBook'
                self.device['type'] = 'tablet'
                self.device['identified'] = True





        # WebOS
        #

        if optimizedSearch(r'(?:web|hpw)OS', ua):
            self.os['name'] = 'webOS'
            self.os['version'] = Version({
                'value': optimizedSearch(r'(?:web|hpw)OS\/([0-9.]*)', ua).groups(1),
            })

            if 'tablet' in ua:
                self.device['type'] = 'tablet'
            else:
                self.device['type'] = 'mobile'

            self.device['manufacturer'] = 'HP' if 'hpwOS' in ua else 'Palm'
            tmpMap = {
                'Pre\/1.0': 'Pre',
                'Pre\/1.1': 'Pre Plus',
                'Pre\/1.2': 'Pre2',
                'Pre\/3.0': 'Pre3',
                'Pixi\/1.0': 'Pixi',
                'Pixi\/1.1': 'Pixi Plus',
                'P160UN?A?\/1.0': 'Veer',
                'TouchPad\/1.0': 'TouchPad'
            }
            for item in tmpMap.keys():
                if optimizedSearch(item, ua):
                    self.device['model'] = tmpMap[item]
            # origin
            # if ua.match('Pre\/1.0')) self.device['model'] = 'Pre'
            # if ua.match('Pre\/1.1')) self.device['model'] = 'Pre Plus'
            # if ua.match('Pre\/1.2')) self.device['model'] = 'Pre2'
            # if ua.match('Pre\/3.0')) self.device['model'] = 'Pre3'
            # if ua.match('Pixi\/1.0')) self.device['model'] = 'Pixi'
            # if ua.match('Pixi\/1.1')) self.device['model'] = 'Pixi Plus'
            # if ua.match('P160UN?A?\/1.0')) self.device['model'] = 'Veer'
            # if ua.match('TouchPad\/1.0')) self.device['model'] = 'TouchPad'

            if optimizedSearch(r'Emulator\/', ua) or optimizedSearch(r'Desktop\/', ua):
                self.device['type'] = 'emulator'
                self.device['manufacturer'] = None
                self.device['model'] = None


            self.device['identified'] = True



        # S60
        #
        # fix S60可能是联想手机: Lenovo S60-t/V2.0 Linux/3.4.5 Android/4.4 Release/10.08.2014 Browser/AppleWebKit537.36 Chrome/30.0.0.0 Mobile Safari/537.36; 124
        if 'Symbian' in ua or optimizedSearch(r'Series[ ]?60', ua) or ('S60' in ua and 'Android' not in ua):
            self.os['name'] = 'Series60'

            if optimizedSearch(r'SymbianOS/9.1', ua) and not optimizedSearch(r'Series60', ua):
                self.os['version'] = Version({
                    'value': '3.0'
                })

            match = optimizedSearch(r'Series60\/([0-9.]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })

            match = optimizedSearch(r'Nokia([^\/;]+)[\/|;]', ua)
            if match:
                if match.group(1) is not 'Browser':
                    self.device['manufacturer'] = 'Nokia'
                    self.device['model'] = match.group(1)
                    self.device['identified'] = True


            match = optimizedSearch(r'Vertu([^\/;]+)[\/|;]', ua)
            if match:
                self.device['manufacturer'] = 'Vertu'
                self.device['model'] = match.group(1)
                self.device['identified'] = True

            match = optimizedSearch(r'Symbian; U; ([^;]+); [a-z][a-z]\-[a-z][a-z]', ua, re.I)
            if match:
                self.device['manufacturer'] = 'Nokia'
                self.device['model'] = match.group(1)
                self.device['identified'] = True

            match = optimizedSearch(r'Samsung\/([^;]*);', ua)
            if match:
                self.device['manufacturer'] = STRINGS_SAMSUNG
                self.device['model'] = match.group(1)
                self.device['identified'] = True


            self.device['type'] = 'mobile'



        # S40
        #

        if 'Series40' in ua:
            self.os['name'] = 'Series40'
            match = optimizedSearch(r'Nokia([^\/]+)\/', ua)
            if match:
                self.device['manufacturer'] = 'Nokia'
                self.device['model'] = match.group(1)
                self.device['identified'] = True


            self.device['type'] = 'mobile'



        # MeeGo
        #

        if 'MeeGo' in ua:
            self.os['name'] = 'MeeGo'
            self.device['type'] = 'mobile'
            match = optimizedSearch(r'Nokia([^\)]+)\)', ua)
            if match:
                self.device['manufacturer'] = 'Nokia'
                self.device['model'] = match.group(1)
                self.device['identified'] = True




        # Maemo
        #

        if 'Maemo' in ua:
            self.os['name'] = 'Maemo'
            self.device['type'] = 'mobile'
            match = optimizedSearch(r'(N[0-9]+)', ua)
            if match:
                self.device['manufacturer'] = 'Nokia'
                self.device['model'] = match.group(1)
                self.device['identified'] = True




        # Tizen
        #

        if 'Tizen' in ua:
            self.os['name'] = 'Tizen'
            match = optimizedSearch(r'Tizen[\/ ]([0-9.]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })


            self.device['type'] = 'mobile'
            match = optimizedSearch(r'\(([^;]+); ([^\/]+)\/', ua)
            if match:
                if match.group(1) is not 'Linux':
                    self.device['manufacturer'] = match.group(1)
                    self.device['model'] = match.group(2)

                    if self.device['manufacturer'] in TIZEN_MODELS and self.device['model'] in TIZEN_MODELS[self.device['manufacturer']]:
                        manufacturer = self.device['manufacturer']
                        model = cleanupModel(self.device['model'])

                        self.device['manufacturer'] = TIZEN_MODELS[manufacturer][model][0]
                        self.device['model'] = TIZEN_MODELS[manufacturer][model][1]
                        self.device['identified'] = True






        # Bada
        #
        if optimizedSearch(r'[b|B]ada', ua):
            self.os['name'] = 'Bada'
            match = optimizedSearch(r'[b|B]ada\/([0-9.]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })


            self.device['type'] = 'mobile'
            match = optimizedSearch(r'\(([^;]+); ([^\/]+)\/', ua)
            if match:
                self.device['manufacturer'] = match.group(1)
                self.device['model'] = cleanupModel(match.group(2))

            if self.device['manufacturer'] in BADA_MODELS and self.device['model'] in BADA_MODELS[self.device['manufacturer']]:
                manufacturer = self.device['manufacturer']
                model = cleanupModel(self.device['model'])

                self.device['manufacturer'] = BADA_MODELS[manufacturer][model][0]
                self.device['model'] = BADA_MODELS[manufacturer][model][1]
                self.device['identified'] = True




        # Brew
        #

        if optimizedSearch(r'BREW', ua, re.I) or optimizedSearch(r'BMP; U', ua):
            self.os['name'] = 'Brew'
            self.device['type'] = 'mobile'
            match = optimizedSearch(r'BREW; U; ([0-9.]*)', ua, re.I)
            match1 = optimizedSearch(r';BREW\/([0-9.]*)', ua, re.I)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })
            elif match1:
                self.os['version'] = Version({
                    'value': match1.group(1)
                })


            match = optimizedSearch(r'\(([^;]+);U;REX\/[^;]+;BREW\/[^;]+;(?:.*;)?[0-9]+\*[0-9]+;CTC\/2.0\)', ua)
            if match:
                self.device['model'] = match.group(1)


            if self.device['model']:
                model = cleanupModel(self.device['model'])

                if model in BREW_MODELS:
                    self.device['manufacturer'] = BREW_MODELS[model][0]
                    self.device['model'] = BREW_MODELS[model][1]
                    self.device['identified'] = True





        # MTK
        #

        if optimizedSearch(r'\(MTK;', ua):
            self.os['name'] = 'MTK'
            self.device['type'] = 'mobile'



        # CrOS
        #

        if 'CrOS' in ua:
            self.os['name'] = 'Chrome OS'
            self.device['type'] = 'desktop'



        # Joli OS
        #

        if 'Joli OS' in ua:
            self.os['name'] = 'Joli OS'
            self.device['type'] = 'desktop'
            match = optimizedSearch(r'Joli OS\/([0-9.]*)', ua, re.I)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })




        # Haiku
        #

        if 'Haiku' in ua:
            self.os['name'] = 'Haiku'
            self.device['type'] = 'desktop'



        # QNX
        #

        if 'QNX' in ua:
            self.os['name'] = 'QNX'
            self.device['type'] = 'mobile'



        # OS/2 Warp
        #

        if optimizedSearch(r'OS\/2; Warp', ua):
            self.os['name'] = 'OS/2 Warp'
            self.device['type'] = 'desktop'
            match = optimizedSearch(r'OS\/2; Warp ([0-9.]*)', ua, re.I)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })




        # Grid OS
        #

        if 'Grid OS' in ua:
            self.os['name'] = 'Grid OS'
            self.device['type'] = 'tablet'
            match = optimizedSearch(r'Grid OS ([0-9.]*)', ua, re.I)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })




        # AmigaOS
        #

        if optimizedSearch(r'AmigaOS', ua, re.I):
            self.os['name'] = 'AmigaOS'
            self.device['type'] = 'desktop'
            match = optimizedSearch(r'AmigaOS ([0-9.]*)', ua, re.I)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })





        # MorphOS
        #

        if optimizedSearch(r'MorphOS', ua, re.I):
            self.os['name'] = 'MorphOS'
            self.device['type'] = 'desktop'
            match = optimizedSearch(r'MorphOS ([0-9.]*)', ua, re.I)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })





        # Kindle
        #

        if 'Kindle' in ua and 'Fire' not in ua:
            self.os['name'] = ''

            self.device['manufacturer'] = 'Amazon'
            self.device['model'] = 'Kindle'
            self.device['type'] = 'ereader'

            if optimizedSearch(r'Kindle\/2.0', ua):
                self.device['model'] = 'Kindle 2'
            if optimizedSearch(r'Kindle\/3.0', ua):
                self.device['model'] = 'Kindle 3 or later'

            self.device['identified'] = True



        # NOOK
        #

        if 'nook browser' in ua:
            self.os['name'] = 'Android'

            self.device['manufacturer'] = 'Barnes & Noble'
            self.device['model'] = 'NOOK'
            self.device['type'] = 'ereader'
            self.device['identified'] = True



        # Bookeen
        #

        if optimizedSearch(r'bookeen\/cybook', ua):
            self.os['name'] = ''

            self.device['manufacturer'] = 'Bookeen'
            self.device['model'] = 'Cybook'
            self.device['type'] = 'ereader'

            if 'Orizon' in ua:
                self.device['model'] = 'Cybook Orizon'


            self.device['identified'] = True



        # Sony Reader
        #

        if 'EBRD1101' in ua:
            self.os['name'] = ''

            self.device['manufacturer'] = 'Sony'
            self.device['model'] = 'Reader'
            self.device['type'] = 'ereader'
            self.device['identified'] = True



        # iRiver
        #

        if 'Iriver ;' in ua:
            self.os['name'] = ''

            self.device['manufacturer'] = 'iRiver'
            self.device['model'] = 'Story'
            self.device['type'] = 'ereader'

            if 'EB07' in ua:
                self.device['model'] = 'Story HD EB07'


            self.device['identified'] = True



        # Nintendo
        #
        # Opera/9.30 (Nintendo Wii; U; ; 3642; en)
        # Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)
        # Opera/9.50 (Nintendo DSi; Opera/507; U; en-US)
        # Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7455.US
        # Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7455.EU
        #

        if 'Nintendo Wii' in ua:
            self.os['name'] = ''

            self.device['manufacturer'] = 'Nintendo'
            self.device['model'] = 'Wii'
            self.device['type'] = 'gaming'
            self.device['identified'] = True


        if 'Nintendo DSi' in ua:
            self.os['name'] = ''

            self.device['manufacturer'] = 'Nintendo'
            self.device['model'] = 'DSi'
            self.device['type'] = 'gaming'
            self.device['identified'] = True


        if 'Nintendo 3DS' in ua:
            self.os['name'] = ''

            self.device['manufacturer'] = 'Nintendo'
            self.device['model'] = '3DS'
            self.device['type'] = 'gaming'
            match = optimizedSearch(r'Version\/([0-9.]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })


            self.device['identified'] = True



        if 'PlayStation Portable' in ua:
            self.os['name'] = ''

            self.device['manufacturer'] = 'Sony'
            self.device['model'] = 'Playstation Portable'
            self.device['type'] = 'gaming'
            self.device['identified'] = True


        if 'PlayStation Vita' in ua:
            self.os['name'] = ''
            match = optimizedSearch(r'PlayStation Vita ([0-9.]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })


            self.device['manufacturer'] = 'Sony'
            self.device['model'] = 'PlayStation Vita'
            self.device['type'] = 'gaming'
            self.device['identified'] = True


        if optimizedSearch(r'PlayStation 3', ua, re.I):
            self.os['name'] = ''
            match = optimizedSearch(r'PLAYSTATION 3;? ([0-9.]*)', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1)
                })


            self.device['manufacturer'] = 'Sony'
            self.device['model'] = 'Playstation 3'
            self.device['type'] = 'gaming'
            self.device['identified'] = True



        # Panasonic Smart Viera
        #
        # Mozilla/5.0 (FreeBSD; U; Viera; ja-JP) AppleWebKit/535.1 (KHTML, like Gecko) Viera/1.2.4 Chrome/14.0.835.202 Safari/535.1
        #

        if 'Viera' in ua:
            self.os['name'] = ''
            self.device['manufacturer'] = 'Panasonic'
            self.device['model'] = 'Smart Viera'
            self.device['type'] = 'television'
            self.device['identified'] = True




        # Sharp AQUOS TV
        #
        # Mozilla/5.0 (DTV) AppleWebKit/531.2  (KHTML, like Gecko) AQUOSBrowser/1.0 (US00DTV;V;0001;0001)
        # Mozilla/5.0 (DTV) AppleWebKit/531.2+ (KHTML, like Gecko) Espial/6.0.4 AQUOSBrowser/1.0 (CH00DTV;V;0001;0001)
        # Opera/9.80 (Linux armv6l; U; en) Presto/2.8.115 Version/11.10 AQUOS-AS/1.0 LC-40LE835X
        #

        if 'AQUOSBrowser' in ua or 'AQUOS-AS' in ua:
            self.os['name'] = ''
            self.device['manufacturer'] = STRINGS_SHARP
            self.device['model'] = 'Aquos TV'
            self.device['type'] = 'television'
            self.device['identified'] = True




        # Samsung Smart TV
        #
        # Mozilla/5.0 (SmartHub; SMART-TV; U; Linux/SmartTV; Maple2012) AppleWebKit/534.7 (KHTML, like Gecko) SmartTV Safari/534.7
        # Mozilla/5.0 (SmartHub; SMART-TV; U; Linux/SmartTV) AppleWebKit/531.2+ (KHTML, like Gecko) WebBrowser/1.0 SmartTV Safari/531.2+
        #

        if 'SMART-TV' in ua:
            self.os['name'] = ''
            self.device['manufacturer'] = STRINGS_SAMSUNG
            self.device['model'] = 'Smart TV'
            self.device['type'] = 'television'
            self.device['identified'] = True
            match = optimizedSearch(r'Maple([0-9]*)', ua)
            if match:
                self.device['model'] += ' ' + match.group(1)




        # Sony Internet TV
        #
        # Opera/9.80 (Linux armv7l; U; InettvBrowser/2.2(00014A;SonyDTV115;0002;0100) KDL-46EX640; CC/USA; en) Presto/2.8.115 Version/11.10
        # Opera/9.80 (Linux armv7l; U; InettvBrowser/2.2(00014A;SonyDTV115;0002;0100) KDL-40EX640; CC/USA; en) Presto/2.10.250 Version/11.60
        # Opera/9.80 (Linux armv7l; U; InettvBrowser/2.2(00014A;SonyDTV115;0002;0100) N/A; CC/USA; en) Presto/2.8.115 Version/11.10
        # Opera/9.80 (Linux mips; U; InettvBrowser/2.2 (00014A;SonyDTV115;0002;0100) ; CC/JPN; en) Presto/2.9.167 Version/11.50
        # Opera/9.80 (Linux mips; U; InettvBrowser/2.2 (00014A;SonyDTV115;0002;0100) AZ2CVT2; CC/CAN; en) Presto/2.7.61 Version/11.00
        # Opera/9.80 (Linux armv6l; Opera TV Store/4207; U; (SonyBDP/BDV11); en) Presto/2.9.167 Version/11.50
        # Opera/9.80 (Linux armv6l ; U; (SonyBDP/BDV11); en) Presto/2.6.33 Version/10.60
        # Opera/9.80 (Linux armv6l; U; (SonyBDP/BDV11); en) Presto/2.8.115 Version/11.10
        #

        if optimizedSearch(r'SonyDTV|SonyBDP|SonyCEBrowser', ua):
            self.os['name'] = ''
            self.device['manufacturer'] = 'Sony'
            self.device['model'] = 'Internet TV'
            self.device['type'] = 'television'
            self.device['identified'] = True



        # Philips Net TV
        #
        # Opera/9.70 (Linux armv6l ; U; CE-HTML/1.0 NETTV/2.0.2; en) Presto/2.2.1
        # Opera/9.80 (Linux armv6l ; U; CE-HTML/1.0 NETTV/3.0.1;; en) Presto/2.6.33 Version/10.60
        # Opera/9.80 (Linux mips; U; CE-HTML/1.0 NETTV/3.0.1; PHILIPS-AVM-2012; en) Presto/2.9.167 Version/11.50
        # Opera/9.80 (Linux mips ; U; HbbTV/1.1.1 (; Philips; ; ; ; ) CE-HTML/1.0 NETTV/3.1.0; en) Presto/2.6.33 Version/10.70
        # Opera/9.80 (Linux i686; U; HbbTV/1.1.1 (; Philips; ; ; ; ) CE-HTML/1.0 NETTV/3.1.0; en) Presto/2.9.167 Version/11.50
        #

        if optimizedSearch(r'NETTV\/', ua):
            self.os['name'] = ''
            self.device['manufacturer'] = 'Philips'
            self.device['model'] = 'Net TV'
            self.device['type'] = 'television'
            self.device['identified'] = True



        # LG NetCast TV
        #
        # Mozilla/5.0 (DirectFB; Linux armv7l) AppleWebKit/534.26+ (KHTML, like Gecko) Version/5.0 Safari/534.26+ LG Browser/5.00.00(+mouse+3D+SCREEN+TUNER; LGE; GLOBAL-PLAT4; 03.09.22; 0x00000001;); LG NetCast.TV-2012
        # Mozilla/5.0 (DirectFB; Linux armv7l) AppleWebKit/534.26+ (KHTML, like Gecko) Version/5.0 Safari/534.26+ LG Browser/5.00.00(+SCREEN+TUNER; LGE; GLOBAL-PLAT4; 01.00.00; 0x00000001;); LG NetCast.TV-2012
        # Mozilla/5.0 (DirectFB; U; Linux armv6l; en) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  LG Browser/4.1.4( BDP; LGE; Media/BD660; 6970; abc;); LG NetCast.Media-2011
        # Mozilla/5.0 (DirectFB; U; Linux 7631; en) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  LG Browser/4.1.4( NO_NUM; LGE; Media/SP520; ST.3.97.409.F; 0x00000001;); LG NetCast.Media-2011
        # Mozilla/5.0 (DirectFB; U; Linux 7630; en) AppleWebKit/531.2  (KHTML, like Gecko) Safari/531.2  LG Browser/4.1.4( 3D BDP NO_NUM; LGE; Media/ST600; LG NetCast.Media-2011
        # (LGSmartTV/1.0) AppleWebKit/534.23 OBIGO-T10/2.0
        #
        match = optimizedSearch(r'LG NetCast\.(?:TV|Media)-([0-9]*)', ua)
        if match:
            self.os['name'] = ''
            self.device['manufacturer'] = STRINGS_LG
            self.device['model'] = 'NetCast TV ' + match.group(1)
            self.device['type'] = 'television'
            self.device['identified'] = True

        match = optimizedSearch(r'LGSmartTV', ua)
        if match:
            self.os['name'] = ''
            self.device['manufacturer'] = STRINGS_LG
            self.device['model'] = 'Smart TV'
            self.device['type'] = 'television'
            self.device['identified'] = True



        # Toshiba Smart TV
        #
        # Mozilla/5.0 (Linux mipsel; U; HbbTV/1.1.1 (; TOSHIBA; DTV_RL953; 56.7.66.7; t12; ) ; ToshibaTP/1.3.0 (+VIDEO_MP4+VIDEO_X_MS_ASF+AUDIO_MPEG+AUDIO_MP4+DRM+NATIVELAUNCH) ; en) AppleWebKit/534.1 (KHTML, like Gecko)
        # Mozilla/5.0 (DTV; TSBNetTV/T32013713.0203.7DD; TVwithVideoPlayer; like Gecko) NetFront/4.1 DTVNetBrowser/2.2 (000039;T32013713;0203;7DD) InettvBrowser/2.2 (000039;T32013713;0203;7DD)
        # Mozilla/5.0 (Linux mipsel; U; HbbTV/1.1.1 (; TOSHIBA; 40PX200; 0.7.3.0.; t12; ) ; Toshiba_TP/1.3.0 (+VIDEO_MP4+AUDIO_MPEG+AUDIO_MP4+VIDEO_X_MS_ASF+OFFLINEAPP) ; en) AppleWebKit/534.1 (KHTML, like Gec
        #

        if optimizedSearch(r'Toshiba_?TP\/', ua) or optimizedSearch(r'TSBNetTV\/', ua):
            self.os['name'] = ''
            self.device['manufacturer'] = 'Toshiba'
            self.device['model'] = 'Smart TV'
            self.device['type'] = 'television'
            self.device['identified'] = True



        # MachBlue XT
        #
        match = optimizedSearch(r'mbxtWebKit\/([0-9.]*)', ua)
        if match:
            self.os['name'] = ''
            self.browser['name'] = 'MachBlue XT'
            self.browser['version'] = Version({
                'value': match.group(1),
                'details': 2
            })
            self.device['type'] = 'television'



        # ADB
        #
        match = optimizedSearch(r'\(ADB; ([^\)]+)\)', ua)
        if match:
            self.os['name'] = ''
            self.device['manufacturer'] = 'ADB'
            self.device['model'] = (match.group(1).replace('ADB', '') + ' ' if match.group(1) is not 'Unknown' else '') + 'IPTV receiver'
            self.device['type'] = 'television'
            self.device['identified'] = True



        # MStar
        #
        if optimizedSearch(r'Mstar;OWB', ua):
            self.os['name'] = ''
            self.device['manufacturer'] = 'MStar'
            self.device['model'] = 'PVR'
            self.device['type'] = 'television'
            self.device['identified'] = True

            self.browser['name'] = 'Origyn Web Browser'



        # TechniSat
        #
        match = optimizedSearch(r'\TechniSat ([^;]+);', ua)
        if match:
            self.os['name'] = ''
            self.device['manufacturer'] = 'TechniSat'
            self.device['model'] = match.group(1)
            self.device['type'] = 'television'
            self.device['identified'] = True



        # Technicolor
        #
        match = optimizedSearch(r'\Technicolor_([^;]+);', ua)
        if match:
            self.os['name'] = ''
            self.device['manufacturer'] = 'Technicolor'
            self.device['model'] = match.group(1)
            self.device['type'] = 'television'
            self.device['identified'] = True



        # Winbox Evo2
        #
        match = optimizedSearch(r'Winbox Evo2', ua)
        if match:
            self.os['name'] = ''
            self.device['manufacturer'] = 'Winbox'
            self.device['model'] = 'Evo2'
            self.device['type'] = 'television'
            self.device['identified'] = True



        # Roku
        #
        match = optimizedSearch(r'^Roku\/DVP-([0-9]+)', ua)
        if match:
            self.device['manufacturer'] = 'Roku'
            self.device['type'] = 'television'
            tmpMap = {
                '2000': 'HD',
                '2050': 'XD',
                '2100': 'XDS',
                '2400': 'LT',
                '3000': '2 HD',
                '3050': '2 XD',
                '3100': '2 XS'
            }
            if match.group(1) in tmpMap:
                self.device['model'] = tmpMap[match.group(1)]

            self.device['identified'] = True

        match = optimizedSearch(r'HbbTV\/1.1.1 \([^;]*;\s*([^;]*)\s*;\s*([^;]*)\s*;', ua)
        if match:
            vendorName = match.group(1).trim()
            modelName = match.group(2).trim()

            if not self.device['manufacturer'] and vendorName is not '' and vendorName is not 'vendorName':
                tmpMap = {
                    'LGE': 'LG',
                    'TOSHIBA': 'Toshiba',
                    'smart': 'Smart',
                    'tv2n': 'TV2N',
                    '3000': '2 HD',
                    '3050': '2 XD',
                    '3100': '2 XS'
                }
                if vendorName in tmpMap:
                    self.device['model'] = tmpMap[vendorName]
                else:
                    self.device['manufacturer'] = vendorName
                # origin
                # switch (vendorName) {
                #     case 'LGE':
                #         self.device['manufacturer'] = 'LG';
                #         break;
                #     case 'TOSHIBA':
                #         self.device['manufacturer'] = 'Toshiba';
                #         break;
                #     case 'smart':
                #         self.device['manufacturer'] = 'Smart';
                #         break;
                #     case 'tv2n':
                #         self.device['manufacturer'] = 'TV2N';
                #         break;
                #     default:
                #         self.device['manufacturer'] = vendorName;
                # }

                if not self.device['model'] and modelName is not '' and modelName is not 'modelName':
                    tmpMap = {
                        'GLOBAL_PLAT3': 'NetCast TV',
                        'SmartTV2012': 'Smart TV 2012',
                        'videoweb': 'Videoweb'
                    }
                    if vendorName in tmpMap:
                        self.device['model'] = tmpMap[vendorName]
                    else:
                        self.device['manufacturer'] = vendorName
                    # origin
                    # switch (modelName) {
                    #     case 'GLOBAL_PLAT3':
                    #         self.device['model'] = 'NetCast TV';
                    #         break;
                    #     case 'SmartTV2012':
                    #         self.device['model'] = 'Smart TV 2012';
                    #         break;
                    #     case 'videoweb':
                    #         self.device['model'] = 'Videoweb';
                    #         break;
                    #     default:
                    #         self.device['model'] = modelName;
                    # }

                    if vendorName is 'Humax':
                        self.device['model'] = self.device['model'].upper()


                    self.device['identified'] = True
                    self.os['name'] = ''



            self.device['type'] = 'television'



        # Detect type based on common identifiers
        #

        if 'InettvBrowser' in ua:
            self.device['type'] = 'television'


        if 'MIDP' in ua:
            self.device['type'] = 'mobile'



        # Try to detect any devices based on common
        # locations of model ids
        #

        if not self.device['model'] and not self.device['manufacturer']:
            candidates = []

            if not optimizedSearch(r'^(Mozilla|Opera)', ua):
                match = optimizedSearch(r'^(?:MQQBrowser\/[0-9\.]+\/)?([^\s]+)', ua)
                if match:
                    tmp = match.group(1)
                    tmp = optimizedSub(r'_TD$', '', tmp, 1)
                    tmp = optimizedSub(r'_CMCC$', '', tmp, 1)
                    tmp = optimizedSub(r'[_ ]Mozilla$', '', tmp, 1)
                    tmp = optimizedSub(r' Linux$', '', tmp, 1)
                    tmp = optimizedSub(r' Opera$', '', tmp, 1)
                    tmp = optimizedSub(r'\/[0-9].*$', '', tmp, 1)

                    # match.group(1) = match.group(1).replace(/_TD$/, '')
                    # match.group(1) = match.group(1).replace(//, '')
                    # match.group(1) = match.group(1).replace(//, '')
                    # match.group(1) = match.group(1).replace(/ Linux$/, '')
                    # match.group(1) = match.group(1).replace(/ Opera$/, '')
                    # match.group(1) = match.group(1).replace(/\/[0-9].*$/, '')

                    candidates.append(tmp)

            match = optimizedSearch(r'[0-9]+x[0-9]+; ([^;]+)', ua)
            if match:
                candidates.append(match.group(1))

            match = optimizedSearch(r'[0-9]+X[0-9]+ ([^;\/\(\)]+)', ua)
            if match:
                candidates.append(match.group(1))

            match = optimizedSearch(r'Windows NT 5.1; ([^;]+); Windows Phone', ua)
            if match:
                candidates.append(match.group(1))

            match = optimizedSearch(r'\) PPC; (?:[0-9]+x[0-9]+; )?([^;\/\(\)]+)', ua)
            if match:
                candidates.append(match.group(1))

            match = optimizedSearch(r'\(([^;]+); U; Windows Mobile', ua)
            if match:
                candidates.append(match.group(1))

            match = optimizedSearch(r'Vodafone\/1.0\/([^\/]+)', ua)
            if match:
                candidates.append(match.group(1))

            match = optimizedSearch(r'\ ([^\s]+)$', ua)
            if match:
                candidates.append(match.group(1))

            for item in candidates:
            # for (i = 0; i < candidates.length; i++) {

                if not self.device['model'] and not self.device['manufacturer']:
                    model = cleanupModel(item)
                    result = False

                    if self.os['name'] is 'Android':
                        if model in ANDROID_MODELS:
                            self.device['manufacturer'] = ANDROID_MODELS[model][0]
                            self.device['model'] = ANDROID_MODELS[model][1]
                            if len(ANDROID_MODELS[model]) > 2:
                                self.device['type'] = ANDROID_MODELS[model][2]
                            self.device['identified'] = True

                            result = True



                    if not self.os['name'] or self.os['name'] is 'Windows' or self.os['name'] is 'Windows Mobile' or self.os['name'] is 'Windows CE':
                        if model in WINDOWS_MOBILE_MODELS:
                            self.device['manufacturer'] = WINDOWS_MOBILE_MODELS[model][0]
                            self.device['model'] = WINDOWS_MOBILE_MODELS[model][1]
                            self.device['type'] = 'mobile'
                            self.device['identified'] = True

                            if self.os['name'] is not 'Windows Mobile':
                                self.os['name'] = 'Windows Mobile'
                                self.os['version'] = None


                            result = True




                if not result:
                    tmpArr = [
                        {
                            'reg': '^GIONEE-([^\s]+)',
                            'manufacturer': 'Gionee'
                        },
                        {
                            'reg': '^HTC_?([^\/_]+)(?:\/|_|$)',
                            'manufacturer': STRINGS_HTC
                        },
                        {
                            'reg': '^HUAWEI-([^\/]*)',
                            'manufacturer': STRINGS_HUAWEI
                        },
                        {
                            'reg': '(?:^|\()LGE?(?:\/|-|_|\s)([^\s]*)',
                            'manufacturer': STRINGS_LG
                        },
                        {
                            'reg': '^MOT-([^\/_]+)(?:\/|_|$)',
                            'manufacturer': STRINGS_MOTOROLA
                        },
                        {
                            'reg': '^Motorola_([^\/_]+)(?:\/|_|$)',
                            'manufacturer': STRINGS_MOTOROLA
                        },
                        {
                            'reg': '^Nokia([^\/]+)(?:\/|$)',
                            'manufacturer': 'Nokia'
                        },
                        {
                            'reg': '^SonyEricsson([^\/_]+)(?:\/|_|$)',
                            'manufacturer': STRINGS_SONY_ERICSSON
                        },

                        {
                            'reg': '^SonyEricsson([^\/_]+)(?:\/|_|$)',
                            'manufacturer': STRINGS_SONY_ERICSSON
                        },
                        {
                            'reg': '^SonyEricsson([^\/_]+)(?:\/|_|$)',
                            'manufacturer': STRINGS_SONY_ERICSSON
                        }
                    ]
                    for row in tmpArr:
                        match = optimizedSearch(row['reg'], item)
                        if match:
                            self.device['manufacturer'] = row['manufacturer']
                            self.device['model'] = cleanupModel(match.group(1))
                            self.device['type'] = 'mobile'
                            self.device['identified'] = True

                            if row['manufacturer'] == 'Nokia' and not self.os['name']:
                                self.os['name'] = 'Series40'

                            break
                    # match = optimizedSearch(r'^HTC_?([^\/_]+)(?:\/|_|$)', item)
                    # if match:
                    #     self.device['manufacturer'] = STRINGS_HTC
                    #     self.device['model'] = cleanupModel(match.group(1))
                    #     self.device['type'] = 'mobile'
                    #     self.device['identified'] = True


                    # if match = //.exec(item):
                    #     self.device['manufacturer'] = STRINGS_HUAWEI
                    #     self.device['model'] = cleanupModel(match.group(1))
                    #     self.device['type'] = 'mobile'
                    #     self.device['identified'] = True


                    # if match = //.exec(item):
                    #     self.device['manufacturer'] = STRINGS_LG
                    #     self.device['model'] = cleanupModel(match.group(1))
                    #     self.device['type'] = 'mobile'
                    #     self.device['identified'] = True


                    # if match = //.exec(item):
                    #     self.device['manufacturer'] = STRINGS_MOTOROLA
                    #     self.device['model'] = cleanupModel(match.group(1))
                    #     self.device['type'] = 'mobile'
                    #     self.device['identified'] = True


                    # if match = //.exec(item):
                    #     self.device['manufacturer'] = STRINGS_MOTOROLA
                    #     self.device['model'] = cleanupModel(match.group(1))
                    #     self.device['type'] = 'mobile'
                    #     self.device['identified'] = True


                    # if match = //.exec(item):
                    #     self.device['manufacturer'] = 'Nokia'
                    #     self.device['model'] = cleanupModel(match.group(1))
                    #     self.device['type'] = 'mobile'
                    #     self.device['identified'] = True

                        # if not self.os['name']:
                        #     self.os['name'] = 'Series40'



                    # if match = //.exec(item):
                    #     self.device['manufacturer'] = STRINGS_SONY_ERICSSON
                    #     self.device['model'] = cleanupModel(match.group(1))
                    #     self.device['type'] = 'mobile'
                    #     self.device['identified'] = True

                    match = optimizedSearch(r'^SAMSUNG-([^\/_]+)(?:\/|_|$)', item)
                    if match:
                        self.device['manufacturer'] = STRINGS_SAMSUNG
                        self.device['model'] = cleanupModel(match.group(1))
                        self.device['type'] = 'mobile'

                        if self.os['name'] is 'Bada':
                            manufacturer = 'SAMSUNG'
                            model = cleanupModel(self.device['model'])

                            if manufacturer in BADA_MODELS and model in BADA_MODELS[manufacturer]:
                                self.device['manufacturer'] = BADA_MODELS[manufacturer][model][0]
                                self.device['model'] = BADA_MODELS[manufacturer][model][1]
                                self.device['identified'] = True

                        elif optimizedSearch(r'Jasmine\/([0-9.]*)', ua):
                            match = optimizedSearch(r'Jasmine\/([0-9.]*)', ua)
                            version = match.group(1)
                            manufacturer = 'SAMSUNG'
                            model = cleanupModel(self.device['model'])

                            if manufacturer in TOUCHWIZ_MODELS and model in TOUCHWIZ_MODELS[manufacturer]:
                                self.device['manufacturer'] = TOUCHWIZ_MODELS[manufacturer][model][0]
                                self.device['model'] = TOUCHWIZ_MODELS[manufacturer][model][1]
                                self.device['identified'] = True

                                self.os['name'] = 'Touchwiz'
                                self.os['version'] = Version({
                                    'value': '2.0'
                                })

                        elif optimizedSearch(r'Dolfin\/([0-9.]*)', ua):
                            match = optimizedSearch(r'Dolfin\/([0-9.]*)', ua)
                            version = match.group(1)
                            manufacturer = 'SAMSUNG'
                            model = cleanupModel(self.device['model'])

                            if manufacturer in BADA_MODELS and model in BADA_MODELS[manufacturer]:
                                self.device['manufacturer'] = BADA_MODELS[manufacturer][model][0]
                                self.device['model'] = BADA_MODELS[manufacturer][model][1]
                                self.device['identified'] = True

                                self.os['name'] = 'Bada'
                                tmpMap = {
                                    '2.0': '1.0',
                                    '2.2': '1.2',
                                    '3.0': '2.0',
                                }
                                if version in tmpMap:
                                    self.os['version'] = Version({
                                        'value': tmpMap[version]
                                    })
                                # origin


                            if manufacturer in TOUCHWIZ_MODELS and model in TOUCHWIZ_MODELS[manufacturer]:
                                self.device['manufacturer'] = TOUCHWIZ_MODELS[manufacturer][model][0]
                                self.device['model'] = TOUCHWIZ_MODELS[manufacturer][model][1]
                                self.device['identified'] = True

                                self.os['name'] = 'Touchwiz'

                                tmpMap = {
                                    '1.0': '1.0',
                                    '1.5': '2.0',
                                    '2.0': '3.0',
                                }
                                if version in tmpMap:
                                    self.os['version'] = Version({
                                        'value': tmpMap[version]
                                    })





            # }


        match = optimizedSearch(r'\((?:LG[-|\/])(.*) (?:Browser\/)?AppleWebkit', ua)
        if match:
            self.device['manufacturer'] = STRINGS_LG
            self.device['model'] = match.group(1)
            self.device['type'] = 'mobile'
            self.device['identified'] = True

        match = optimizedSearch(r'^Mozilla\/5.0 \((?:Nokia|NOKIA)(?:\s?)([^\)]+)\)UC AppleWebkit\(like Gecko\) Safari\/530$', ua)
        if match:
            self.device['manufacturer'] = 'Nokia'
            self.device['model'] = match.group(1)
            self.device['type'] = 'mobile'
            self.device['identified'] = True

            self.os['name'] = 'Series60'





        # Safari
        #

        if 'Safari' in ua:
            if self.os['name'] is 'iOS':
                self.browser['stock'] = True
                self.browser['hidden'] = True
                self.browser['name'] = 'Safari'
                self.browser['version'] = None




            if self.os['name'] is 'Mac OS X' or self.os['name'] is 'Windows':
                self.browser['name'] = 'Safari'
                self.browser['stock'] = self.os['name'] is 'Mac OS X'
                match = optimizedSearch(r'Version\/([0-9\.]+)', ua)
                if match:
                    self.browser['version'] = Version({
                        'value': match.group(1)
                    })

                match = optimizedSearch(r'AppleWebKit\/[0-9\.]+\+', ua)
                if match:
                    self.browser['name'] = 'WebKit Nightly Build'
                    self.browser['version'] = None





        # Internet Explorer
        #

        if 'MSIE' in ua:
            self.browser['name'] = 'Internet Explorer'

            if 'IEMobile' in ua or 'Windows CE' in ua or 'Windows Phone' in ua or 'WP7' in ua:
                self.browser['name'] = 'Mobile Internet Explorer'

            match = optimizedSearch(r'MSIE ([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # Opera
        #
        if optimizedSearch(r'Opera', ua, re.I):
            self.browser['stock'] = False
            self.browser['name'] = 'Opera'
            match = optimizedSearch(r'Opera[\/| ]([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })

            match = optimizedSearch(r'Version\/([0-9.]*)', ua)
            if match:
                if float(match.group(1)) >= 10:
                    self.browser['version'] = Version({
                        'value': match.group(1)
                    })
                else:
                    self.browser['version'] = None



            if self.browser['version'] and 'Edition Labs' in ua:
                self.browser['version'].type = 'alpha'
                self.browser['channel'] = 'Labs'


            if self.browser['version'] and 'Edition Next' in ua:
                self.browser['version'].type = 'alpha'
                self.browser['channel'] = 'Next'


            if 'Opera Tablet' in ua:
                self.browser['name'] = 'Opera Mobile'
                self.device['type'] = 'tablet'


            if 'Opera Mobi' in ua:
                self.browser['name'] = 'Opera Mobile'
                self.device['type'] = 'mobile'

            match = optimizedSearch(r'Opera Mini;', ua)
            if match:
                self.browser['name'] = 'Opera Mini'
                self.browser['version'] = None
                self.browser['mode'] = 'proxy'
                self.device['type'] = 'mobile'

            match = optimizedSearch(r'Opera Mini\/(?:att\/)?([0-9.]*)', ua)
            if match:
                self.browser['name'] = 'Opera Mini'
                self.browser['version'] = Version({
                    'value': match.group(1),
                    'details': -1
                })
                self.browser['mode'] = 'proxy'
                self.device['type'] = 'mobile'


            if self.browser['name'] is 'Opera' and self.device['type'] is 'mobile':
                self.browser['name'] = 'Opera Mobile'
                if 'BER' in ua:
                    self.browser['name'] = 'Opera Mini'
                    self.browser['version'] = None



            if 'InettvBrowser' in ua:
                self.device['type'] = 'television'


            if 'Opera TV' in ua or 'Opera-TV' in ua:
                self.browser['name'] = 'Opera'
                self.device['type'] = 'television'


            if 'Linux zbov' in ua:
                self.browser['name'] = 'Opera Mobile'
                self.browser['mode'] = 'desktop'

                self.device['type'] = 'mobile'

                self.os['name'] = None
                self.os['version'] = None


            if 'Linux zvav' in ua:
                self.browser['name'] = 'Opera Mini'
                self.browser['version'] = None
                self.browser['mode'] = 'desktop'

                self.device['type'] = 'mobile'

                self.os['name'] = None
                self.os['version'] = None




        # Firefox
        #

        if 'Firefox' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'Firefox'
            match = optimizedSearch(r'Firefox\/([0-9ab.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })


            if self.browser['version'].type is 'alpha':
                self.browser['channel'] = 'Aurora'


            if self.browser['version'].type is 'beta':
                self.browser['channel'] = 'Beta'


            if 'Fennec' in ua:
                self.device['type'] = 'mobile'


            if 'Mobile; rv' in ua:
                self.device['type'] = 'mobile'


            if 'Tablet; rv' in ua:
                self.device['type'] = 'tablet'


            if self.device['type'] is 'mobile' or self.device['type'] is 'tablet':
                self.browser['name'] = 'Firefox Mobile'



        if 'Namoroka' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'Firefox'
            match = optimizedSearch(r'Namoroka\/([0-9ab.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })


            self.browser['channel'] = 'Namoroka'


        if 'Shiretoko' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'Firefox'
            match = optimizedSearch(r'Shiretoko\/([0-9ab.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })


            self.browser['channel'] = 'Shiretoko'


        if 'Minefield' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'Firefox'
            match = optimizedSearch(r'Minefield\/([0-9ab.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })


            self.browser['channel'] = 'Minefield'


        if 'Firebird' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'Firebird'
            match = optimizedSearch(r'Firebird\/([0-9ab.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # SeaMonkey
        #

        if 'SeaMonkey' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'SeaMonkey'
            match = optimizedSearch(r'SeaMonkey\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # Netscape
        #

        if 'Netscape' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'Netscape'
            match = optimizedSearch(r'Netscape[0-9]?\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # Konqueror
        #

        if optimizedSearch(r'[k|K]onqueror/', ua):
            self.browser['name'] = 'Konqueror'
            match = optimizedSearch(r'[k|K]onqueror\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # Chrome
        #
        match = optimizedSearch(r'(?:Chrome|CrMo|CriOS)\/([0-9.]*)', ua)
        if match:
            self.browser['stock'] = False
            self.browser['name'] = 'Chrome'
            self.browser['version'] = Version({
                'value': match.group(1)
            })

            tmp = '.'.join(match.group(1).split('.', 2))
            if self.os['name'] is 'Android':
                if tmp == '16.0.912':
                    self.browser['channel'] = 'Beta'
                elif tmp == '18.0.1025':
                    self.browser['version'].details = 1
                else:
                    self.browser['channel'] = 'Nightly'
                # switch () {
                #     case '16.0.912':
                #         self.browser['channel'] = 'Beta';
                #         break;
                #     case '18.0.1025':
                #         self.browser['version'].details = 1;
                #         break;
                #     default:
                #         self.browser['channel'] = 'Nightly';
                #         break;
                # }
            else:
                # origin
                # switch (match.group(1).split('.', 3).join('.')) {
                tmpArr = [
                    '0.2.149',
                    '0.3.154',
                    '0.4.154',
                    '1.0.154',
                    '2.0.172',
                    '3.0.195',
                    '4.0.249',
                    '4.1.249',
                    '5.0.375',
                    '6.0.472',
                    '7.0.517',
                    '8.0.552',
                    '9.0.597',
                    '10.0.648',
                    '11.0.696',
                    '12.0.742',
                    '13.0.782',
                    '14.0.835',
                    '15.0.874',
                    '16.0.912',
                    '17.0.963',
                    '18.0.1025',
                    '19.0.1084',
                    '20.0.1132',
                    '21.0.1180'
                ]
                if tmp in tmpArr:
                    if self.browser['version'].minor == 0:
                        self.browser['version'].details = 1
                    else:
                        self.browser['version'].details = 2
                else:
                    self.browser['channel'] = 'Nightly'



        # Chrome Frame
        #

        if 'chromeframe' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'Chrome Frame'
            match = optimizedSearch(r'chromeframe\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # Chromium
        #

        if 'Chromium' in ua:
            self.browser['stock'] = False
            self.browser['channel'] = ''
            self.browser['name'] = 'Chromium'
            match = optimizedSearch(r'Chromium\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # BrowserNG
        #

        if 'BrowserNG' in ua:
            self.browser['name'] = 'Nokia Browser'
            match = optimizedSearch(r'BrowserNG\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1),
                    'details': 3,
                    builds: False
                })




        # Nokia Browser
        #

        if 'NokiaBrowser' in ua:
            self.browser['name'] = 'Nokia Browser'
            match = optimizedSearch(r'NokiaBrowser\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1),
                    'details': 3
                })




        # MicroB
        #

        if optimizedSearch(r'Maemo[ |_]Browser', ua):
            self.browser['name'] = 'MicroB'
            match = optimizedSearch(r'Maemo[ |_]Browser[ |_]([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1),
                    'details': 3
                })





        # NetFront
        #

        if 'NetFront' in ua:
            self.browser['name'] = 'NetFront'
            self.device['type'] = 'mobile'
            match = optimizedSearch(r'NetFront\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })


            if 'InettvBrowser' in ua:
                self.device['type'] = 'television'




        # Silk
        #

        if 'Silk' in ua:
            if 'Silk-Accelerated' in ua:
                self.browser['name'] = 'Silk'
                match = optimizedSearch(r'Silk\/([0-9.]*)', ua)
                if match:
                    self.browser['version'] = Version({
                        'value': match.group(1),
                        'details': 2
                    })


                self.device['manufacturer'] = 'Amazon'
                self.device['model'] = 'Kindle Fire'
                self.device['type'] = 'tablet'
                self.device['identified'] = True

                if self.os['name'] is not 'Android':
                    self.os['name'] = 'Android'
                    self.os['version'] = None





        # Dolfin
        #

        if 'Dolfin' in ua:
            self.browser['name'] = 'Dolfin'
            match = optimizedSearch(r'Dolfin\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })





        # Iris
        #

        if 'Iris' in ua:
            self.browser['name'] = 'Iris'

            self.device['type'] = 'mobile'
            self.device['model'] = None
            self.device['manufacturer'] = None

            self.os['name'] = 'Windows Mobile'
            self.os['version'] = None
            match = optimizedSearch(r'Iris\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })

            match = optimizedSearch(r' WM([0-9]) ', ua)
            if match:
                self.os['version'] = Version({
                    'value': match.group(1) + '.0'
                })
            else:
                self.browser['mode'] = 'desktop'




        # Jasmine
        #

        if 'Jasmine' in ua:
            self.browser['name'] = 'Jasmine'
            match = optimizedSearch(r'Jasmine\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # Boxee
        #

        if 'Boxee' in ua:
            self.browser['name'] = 'Boxee'
            self.device['type'] = 'television'
            match = optimizedSearch(r'Boxee\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # Espial
        #

        if 'Espial' in ua:
            self.browser['name'] = 'Espial'

            self.os['name'] = ''
            self.os['version'] = None

            if self.device['type'] is not 'television':
                self.device['type'] = 'television'
                self.device['model'] = None
                self.device['manufacturer'] = None

            match = optimizedSearch(r'Espial\/([0-9.]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })




        # ANT Galio
        #
        match = optimizedSearch(r'ANTGalio\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'ANT Galio'
            self.browser['version'] = Version({
                'value': match.group(1),
                'details': 3
            })
            self.device['type'] = 'television'



        # NetFront NX
        #
        match = optimizedSearch(r'NX\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'NetFront NX'
            self.browser['version'] = Version({
                'value': match.group(1),
                'details': 2
            })
            match = optimizedSearch(r'DTV', ua, re.I)
            if match:
                self.device['type'] = 'television'
            elif optimizedSearch(r'mobile', ua, re.I):
                self.device['type'] = 'mobile'
            else:
                self.device['type'] = 'desktop'


            self.os['name'] = None
            self.os['version'] = None



        # Obigo
        #
        match = optimizedSearch(r'Obigo', ua, re.I)
        if match:
            self.browser['name'] = 'Obigo'
            match = optimizedSearch(r'Obigo\/([0-9.]*)', ua, re.I)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1)
                })

            match = optimizedSearch(r'Obigo\/([A-Z])([0-9.]*)', ua, re.I)
            if match:
                self.browser['name'] = 'Obigo ' + match.group(1)
                self.browser['version'] = Version({
                    'value': match.group(2)
                })

            match = optimizedSearch(r'Obigo-([A-Z])([0-9.]*)\/', ua, re.I)
            if match:
                self.browser['name'] = 'Obigo ' + match.group(1)
                self.browser['version'] = Version({
                    'value': match.group(2)
                })




        # UC Web
        #

        if 'UCWEB' in ua:
            self.browser['stock'] = False
            self.browser['name'] = 'UC Browser'
            match = optimizedSearch(r'UCWEB([0-9]*[.][0-9]*)', ua)
            if match:
                self.browser['version'] = Version({
                    'value': match.group(1),
                    'details': 3
                })


            if self.os['name'] is 'Linux':
                self.os['name'] = ''


            self.device['type'] = 'mobile'
            match = optimizedSearch(r'^IUC \(U;\s?iOS ([0-9\.]+);', ua)
            if match:
                self.os['name'] = 'iOS'
                self.os['version'] = Version({
                    'value': match.group(1)
                })

            match = optimizedSearch(r'^JUC \(Linux; U; ([0-9\.]+)[^;]*; [^;]+; ([^;]*[^\s])\s*; [0-9]+\*[0-9]+\)', ua)
            if match:
                model = cleanupModel(match.group(2))

                self.os['name'] = 'Android'
                self.os['version'] = Version({
                    'value': match.group(1)
                })

                if model in ANDROID_MODELS:
                    self.device['manufacturer'] = ANDROID_MODELS[model][0]
                    self.device['model'] = ANDROID_MODELS[model][1]
                    if len(ANDROID_MODELS[model]) > 2:
                        self.device['type'] = ANDROID_MODELS[model][2]
                    self.device['identified'] = True



        match = optimizedSearch(r'\) UC ', ua)
        if match:
            self.browser['stock'] = False
            self.browser['name'] = 'UC Browser'

        match = optimizedSearch(r'UCBrowser\/([0-9.]*)', ua)
        if match:
            self.browser['stock'] = False
            self.browser['name'] = 'UC Browser'
            self.browser['version'] = Version({
                'value': match.group(1),
                'details': 2
            })



        # NineSky
        #
        match = optimizedSearch(r'Ninesky(?:-android-mobile(?:-cn)?)?\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'NineSky'
            self.browser['version'] = Version({
                'value': match.group(1)
            })

            if self.os['name'] is not 'Android':
                self.os['name'] = 'Android'
                self.os['version'] = None

                self.device['manufacturer'] = None
                self.device['model'] = None




        # Skyfire
        #
        match = optimizedSearch(r'Skyfire\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'Skyfire'
            self.browser['version'] = Version({
                'value': match.group(1)
            })

            self.device['type'] = 'mobile'

            self.os['name'] = 'Android'
            self.os['version'] = None



        # Dolphin HD
        #
        match = optimizedSearch(r'DolphinHDCN\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'Dolphin'
            self.browser['version'] = Version({
                'value': match.group(1)
            })

            self.device['type'] = 'mobile'

            if self.os['name'] is not 'Android':
                self.os['name'] = 'Android'
                self.os['version'] = None


        match = optimizedSearch(r'Dolphin\/INT', ua)
        if match:
            self.browser['name'] = 'Dolphin'
            self.device['type'] = 'mobile'



        # QQ Browser
        #
        match = optimizedSearch(r'(M?QQBrowser)\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'QQ Browser'

            version = match.group(2)
            if optimizedSearch(r'^[0-9][0-9]$', version):
                version = version[0] + '.' + version[1]

            self.browser['version'] = Version({
                'value': version,
                'details': 2
            })
            self.browser['channel'] = ''

            if not self.os['name'] and match.group(1) is 'QQBrowser':
                self.os['name'] = 'Windows'




        # iBrowser
        #
        match = optimizedSearch(r'(iBrowser)\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'iBrowser'

            version = match.group(2)
            if optimizedSearch(r'[0-9][0-9]', version):
                version = version[0] + '.' + version[1]

            self.browser['version'] = Version({
                'value': version,
                'details': 2
            })
            self.browser['channel'] = ''



        # Puffin
        #
        match = optimizedSearch(r'Puffin\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'Puffin'
            self.browser['version'] = Version({
                'value': match.group(1),
                'details': 2
            })

            self.device['type'] = 'mobile'

            if self.os['name'] is 'Linux':
                self.os['name'] = None
                self.os['version'] = None




        # 360 Extreme Explorer
        #

        if '360EE' in ua:
            self.browser['stock'] = False
            self.browser['name'] = '360 Extreme Explorer'
            self.browser['version'] = None



        # Midori
        #
        match = optimizedSearch(r'Midori\/([0-9.]*)', ua)
        if match:
            self.browser['name'] = 'Midori'
            self.browser['version'] = Version({
                'value': match.group(1)
            })

            if self.os['name'] is not 'Linux':
                self.os['name'] = 'Linux'
                self.os['version'] = None


            self.device['manufacturer'] = None
            self.device['model'] = None
            self.device['type'] = 'desktop'



        # Others
        #
        # 移除browsers

        for item in browsers:
            # 大小写不敏感
            if 'i' in item:
                match = optimizedSearch(item['regexp'], ua, re.I)
            else:
                match = optimizedSearch(item['regexp'], ua)
            if match:
                self.browser['name'] = item['name']
                self.browser['channel'] = ''
                self.browser['stock'] = False

                if len(match.groups()) > 0 and match.group(1):
                    self.browser['version'] = Version({
                        'value': match.group(1),
                        'details': item['details'] if 'details' in item else None
                    })
                else:
                    self.browser['version'] = None





        # WebKit
        #
        match = optimizedSearch(r'WebKit\/([0-9.]*)', ua, re.I)
        if match:
            self.engine['name'] = 'Webkit'
            self.engine['version'] = Version({
                'value': match.group(1)
            })

        match = optimizedSearch(r'Browser\/AppleWebKit([0-9.]*)', ua, re.I)
        if match:
            self.engine['name'] = 'Webkit'
            self.engine['version'] = Version({
                'value': match.group(1)
            })



        # KHTML
        #
        match = optimizedSearch(r'KHTML\/([0-9.]*)', ua)
        if match:
            self.engine['name'] = 'KHTML'
            self.engine['version'] = Version({
                'value': match.group(1)
            })



        # Gecko
        #

        if 'Gecko' in ua and not optimizedSearch(r'like Gecko', ua, re.I):
            self.engine['name'] = 'Gecko'

            match = optimizedSearch(r'; rv:([^\)]+)\)', ua)
            if match:
                self.engine['version'] = Version({
                    'value': match.group(1)
                })




        # Presto
        #
        match = optimizedSearch(r'Presto\/([0-9.]*)', ua)
        if match:
            self.engine['name'] = 'Presto'
            self.engine['version'] = Version({
                'value': match.group(1)
            })



        # Trident
        #
        match = optimizedSearch(r'Trident\/([0-9.]*)', ua)
        if match:
            self.engine['name'] = 'Trident'
            self.engine['version'] = Version({
                'value': match.group(1)
            })

            if self.browser['name'] is 'Internet Explorer':
                if parseVersion(self.engine['version']) is 6 and float(self.browser['version']) < 10:
                    self.browser['version'] = Version({
                        'value': '10.0'
                    })
                    self.browser['mode'] = 'compat'


                if parseVersion(self.engine['version']) is 5 and float(self.browser['version']) < 9:
                    self.browser['version'] = Version({
                        'value': '9.0'
                    })
                    self.browser['mode'] = 'compat'


                if parseVersion(self.engine['version']) is 4 and float(self.browser['version']) < 8:
                    self.browser['version'] = Version({
                        'value': '8.0'
                    })
                    self.browser['mode'] = 'compat'



            if self.os['name'] is 'Windows Phone':
                if parseVersion(self.engine['version']) is 5 and float(self.os['version']) < 7.5:
                    self.os['version'] = Version({
                        'value': '7.5'
                    })






        # Corrections
        #

        if self.os['name'] is 'Android' and self.browser['stock']:
            self.browser['hidden'] = True


        if self.os['name'] is 'iOS' and self.browser['name'] is 'Opera Mini':
            self.os['version'] = None


        if self.browser['name'] is 'Midori' and self.engine['name'] is not 'Webkit':
            self.engine['name'] = 'Webkit'
            self.engine['version'] = None


        if self.device['type'] is 'television' and self.browser['name'] is 'Opera':
            self.browser['name'] = 'Opera Devices'
            tmpMap = {
                '2.10': 3.2,
                '2.9': 3.1,
                '2.8': 3.0,
                '2.7': 2.9,
                '2.6': 2.8,
                '2.4': 10.3,
                '2.3': 10,
                '2.2': 9.7,
                '2.1': 9.6
            }
            if self.engine['version'].original in tmpMap:
                self.browser['version'] = Version({
                    'value': tmpMap[self.engine['version'].original]
                })
            else:
                self.browser['version'] = None

            self.os['name'] = None
            self.os['version'] = None


        # Camouflage
        #

        if self.options['detectCamouflage']:
            match = optimizedSearch(r'Mac OS X 10_6_3; ([^;]+); [a-z]{2}-(?:[a-z]{2})?\)', ua)
            if match:
                self.browser['name'] = ''
                self.browser['version'] = None
                self.browser['mode'] = 'desktop'

                self.os['name'] = 'Android'
                self.os['version'] = None

                self.engine['name'] = 'Webkit'
                self.engine['version'] = None

                self.device['model'] = match.group(1)
                self.device['type'] = 'mobile'

                model = cleanupModel(self.device['model'])
                if model in ANDROID_MODELS:
                    self.device['manufacturer'] = ANDROID_MODELS[model][0]
                    self.device['model'] = ANDROID_MODELS[model][1]
                    if len(ANDROID_MODELS[model]) > 2:
                        self.device['type'] = ANDROID_MODELS[model][2]
                    self.device['identified'] = True


                self.features.append('foundDevice')

            match = optimizedSearch(r'Linux Ventana; [a-z]{2}-[a-z]{2}; (.+) Build', ua)
            if match:
                self.browser['name'] = ''
                self.browser['version'] = None
                self.browser['mode'] = 'desktop'

                self.os['name'] = 'Android'
                self.os['version'] = None

                self.engine['name'] = 'Webkit'
                self.engine['version'] = None

                self.device['model'] = match.group(1)
                self.device['type'] = 'mobile'

                model = cleanupModel(self.device['model'])
                if model in ANDROID_MODELS:
                    self.device['manufacturer'] = ANDROID_MODELS[model][0]
                    self.device['model'] = ANDROID_MODELS[model][1]
                    if len(ANDROID_MODELS[model]) > 2:
                        self.device['type'] = ANDROID_MODELS[model][2]
                    self.device['identified'] = True


                self.features.append('foundDevice')


            if self.browser['name'] is 'Safari':
                # match = optimizedSearch(r'AppleWebKit\/([0-9]+.[0-9]+)', ua, re.I).group(1)
                # optimizedSearch(r'Safari\/([0-9]+.[0-9]+)', ua, re.I).group(1)
                if self.os['name'] is not 'iOS' and optimizedSearch(r'AppleWebKit\/([0-9]+.[0-9]+)', ua, re.I).group(1) is not optimizedSearch(r'Safari\/([0-9]+.[0-9]+)', ua, re.I).group(1):
                    self.features.append('safariMismatch')
                    self.camouflage = True

                # match = optimizedSearch(r'^Mozilla', ua)
                if self.os['name'] is 'iOS' and not optimizedSearch(r'^Mozilla', ua):
                    self.features.append('noMozillaPrefix')
                    self.camouflage = True

                # match = optimizedSearch(r'Version\/[0-9\.]+', ua)
                if not optimizedSearch(r'Version\/[0-9\.]+', ua):
                    self.features.append('noVersion')
                    self.camouflage = True



            if self.browser['name'] is 'Chrome':
                match = optimizedSearch(r'(?:Chrome|CrMo|CriOS)\/([0-9]{1,2}\.[0-9]\.[0-9]{3,4}\.[0-9]+)', ua)
                if not match:
                    self.features.append('wrongVersion')
                    self.camouflage = True



            # 得运行在浏览器里才行的
            # if self.options.useFeatures:
                """If it claims not to be Trident, but it is probably Trident running camouflage mode"""
                # if window.ActiveXObject:
                #     self.features.append('trident')

                #     if self.engine['name'] and self.engine['name'] is not 'Trident':
                #         self.camouflage = self.browser['name'] is None or self.browser['name'] is not 'Maxthon'



                """If it claims not to be Opera, but it is probably Opera running camouflage mode"""
                # if window.opera:
                #     self.features.append('presto')

                #     if self.engine['name'] and self.engine['name'] is not 'Presto':
                #         self.camouflage = True


                #     if self.browser['name'] is 'Internet Explorer':
                #         self.camouflage = True



                """If it claims not to be Gecko, but it is probably Gecko running camouflage mode"""
                # if 'getBoxObjectFor' in document or 'mozInnerScreenX' in window:
                #     self.features.append('gecko')

                #     if self.engine['name'] and self.engine['name'] is not 'Gecko':
                #         self.camouflage = True


                #     if self.browser['name'] is 'Internet Explorer':
                #         self.camouflage = True



                """If it claims not to be Webkit, but it is probably Webkit running camouflage mode"""
                # if 'WebKitCSSMatrix' in window or 'WebKitPoint' in window or 'webkitStorageInfo' in window or 'webkitURL' in window:
                #     self.features.append('webkit')

                #     if self.engine['name'] and self.engine['name'] is not 'Webkit':
                #         self.camouflage = True


                #     if self.browser['name'] is 'Internet Explorer':
                #         self.camouflage = True





                """If it claims to be Safari and uses V8, it is probably an Android device running camouflage mode"""
                # if self.engine['name'] is 'Webkit' and ({}.toString).toString().indexOf('\n') is -1:
                #     self.features.append('v8')

                #     if self.browser is not None and self.browser['name'] is 'Safari':
                #         self.camouflage = True





                """If we have an iPad that is not 768 x 1024, we have an imposter"""
                # if self.device['model'] === 'iPad':
                #     if (screen.width is not 0 and screen.height is not 0) and (screen.width is not 768 and screen.height is not 1024) and (screen.width is not 1024 and screen.height is not 768):
                #         self.features.append('sizeMismatch')
                #         self.camouflage = True



                # """If we have an iPhone or iPod that is not 320 x 480, we have an imposter"""
                # if self.device['model'] === 'iPhone'or self.device['model'] === 'iPod':
                #     if (screen.width is not 0 and screen.height is not 0) and (screen.width is not 320 and screen.height is not 480) and (screen.width is not 480 and screen.height is not 320):
                #         self.features.append('sizeMismatch')
                #         self.camouflage = True




                # if self.os['name'] is 'iOS' and self.os['version']:

                    # if self.os['version'].isOlder('4.0') and 'sandbox' in document.createElement('iframe'):
                    #     self.features.append('foundSandbox')
                    #     self.camouflage = True


                    # if self.os['version'].isOlder('4.2') and 'WebSocket' in window:
                    #     self.features.append('foundSockets')
                    #     self.camouflage = True


                    # if self.os['version'].isOlder('5.0') and not not  window.Worker:
                    #     self.features.append('foundWorker')
                    #     self.camouflage = True


                    # if self.os['version'].isNewer('2.1') and not window.applicationCache:
                    #     self.features.append('noAppCache')
                    #     self.camouflage = True



                # if self.os['name'] is not 'iOS' and self.browser['name'] is 'Safari' and self.browser['version']:

                #     if self.browser['version'].isOlder('4.0') and not not  window.applicationCache:
                #         self.features.append('foundAppCache')
                #         self.camouflage = True


                #     if self.browser['version'].isOlder('4.1') and not not  (window.history and history.pushState):
                #         self.features.append('foundHistory')
                #         self.camouflage = True


                #     if self.browser['version'].isOlder('5.1') and not not  document.documentElement.webkitRequestFullScreen:
                #         self.features.append('foundFullscreen')
                #         self.camouflage = True


                #     if self.browser['version'].isOlder('5.2') and 'FileReader' in window:
                #         self.features.append('foundFileReader')
                #         self.camouflage = True





# };

def cleanupModel(s=''):
    # s = typeof s is 'undefined' ? '' : s

    s = optimizedSub(r'_TD$', '', s, 1)
    s = optimizedSub(r'_CMCC$', '', s, 1)

    s = optimizedSub(r'_', ' ', s)
    s = optimizedSub(r'^\s+|\s+$', '', s)
    s = optimizedSub(r'\/[^/]+$', '', s, 1)
    s = optimizedSub(r'\/[^/]+ Android\/.*', '', s, 1)

    s = optimizedSub(r'^tita on ', '', s, 1)
    s = optimizedSub(r'^Android on ', '', s, 1)
    s = optimizedSub(r'^Android for ', '', s, 1)
    s = optimizedSub(r'^ICS AOSP on ', '', s, 1)
    s = optimizedSub(r'^Full AOSP on ', '', s, 1)
    s = optimizedSub(r'^Full Android on ', '', s, 1)
    s = optimizedSub(r'^Full Cappuccino on ', '', s, 1)
    s = optimizedSub(r'^Full MIPS Android on ', '', s, 1)
    s = optimizedSub(r'^Full Android', '', s, 1)

    s = optimizedSub(r'^Acer ?', '', s, 1, re.I)
    s = optimizedSub(r'^Iconia ', '', s, 1)
    s = optimizedSub(r'^Ainol ', '', s, 1)
    s = optimizedSub(r'^Coolpad ?', 'Coolpad ', s, 1, re.I)
    s = optimizedSub(r'^ALCATEL ', '', s, 1)
    s = optimizedSub(r'^Alcatel OT-(.*)', 'one touch $1', s, 1)
    s = optimizedSub(r'^YL-', '', s, 1)
    s = optimizedSub(r'^Novo7 ?', 'Novo7 ', s, 1, re.I)
    s = optimizedSub(r'^GIONEE ', '', s, 1)
    s = optimizedSub(r'^HW-', '', s, 1)
    s = optimizedSub(r'^Huawei[ -]', 'Huawei ', s, 1, re.I)
    s = optimizedSub(r'^SAMSUNG[ -]', '', s, 1, re.I)
    s = optimizedSub(r'^SonyEricsson', '', s, 1)
    s = optimizedSub(r'^Lenovo Lenovo', 'Lenovo', s, 1)
    s = optimizedSub(r'^LNV-Lenovo', 'Lenovo', s, 1)
    s = optimizedSub(r'^Lenovo-', 'Lenovo ', s, 1)
    s = optimizedSub(r'^(LG)[ _\/]', '$1-', s, 1)
    s = optimizedSub(r'^(HTC.*)\s(?:v|V)?[0-9.]+$', '$1', s, 1)
    s = optimizedSub(r'^(HTC)[-\/]', '$1 ', s, 1)
    s = optimizedSub(r'^(HTC)([A-Z][0-9][0-9][0-9])', '$1 $2', s, 1)
    s = optimizedSub(r'^(Motorola[\s|-])', '', s, 1)
    s = optimizedSub(r'^(Moto|MOT-)', '', s, 1)

    s = optimizedSub(r'-?(orange(-ls)?|vodafone|bouygues)$', '', s, 1, re.I)
    s = optimizedSub(r'http:\/\/.+$', '', s, 1, re.I)

    s = optimizedSub(r'^\s+|\s+$', '', s)

    return s


def parseVersion(version):
    version = str(version) # .toString()
    components = version.split('.')
    major = components.pop(0)
    return float(major + '.' + ''.join(components))


