from version import Version
from utils import optimizedSearch

class BrowserDetector:
    def __init__(self):
        self.browser = {
            'name': '',
            'version': None,
            'mode': '',
            'details': 0,
            'stock': True,
            'hidden': False,
            'channel': ''
        }

        self.engine = {
            'name': '',
            'version': None
        }

    def _detect_engine(self, ua):
        """检测浏览器引擎"""
        # Gecko
        if 'Gecko' in ua and 'like Gecko' not in ua:
            self.engine['name'] = 'Gecko'
            match = optimizedSearch(r'rv:([\d\.]+)', ua)
            if match:
                self.engine['version'] = Version({'value': match.group(1)})

        # Blink (需要放在WebKit检测之前)
        if ('Chrome' in ua or 'Edg/' in ua) and 'AppleWebKit' in ua:
            self.engine['name'] = 'Blink'
            match = optimizedSearch(r'AppleWebKit\/([\d\.]+)', ua)
            if match:
                self.engine['version'] = Version({'value': match.group(1)})

        # WebKit
        elif 'AppleWebKit' in ua:
            self.engine['name'] = 'WebKit'
            match = optimizedSearch(r'AppleWebKit\/([\d\.]+)', ua)
            if match:
                self.engine['version'] = Version({'value': match.group(1)})

        # Presto
        elif 'Presto' in ua:
            self.engine['name'] = 'Presto'
            match = optimizedSearch(r'Presto\/([\d\.]+)', ua)
            if match:
                self.engine['version'] = Version({'value': match.group(1)})

        # Trident
        elif 'Trident' in ua:
            self.engine['name'] = 'Trident'
            match = optimizedSearch(r'Trident\/([\d\.]+)', ua)
            if match:
                self.engine['version'] = Version({'value': match.group(1)})
            # IE 特殊处理
            elif 'MSIE' in ua:
                match = optimizedSearch(r'MSIE ([\d\.]+)', ua)
                if match:
                    version = float(match.group(1))
                    if version >= 7:
                        self.engine['version'] = Version({'value': str(version - 4.0)})

    def detect(self, ua):
        """检测浏览器类型和版本"""
        # 先检测引擎
        self._detect_engine(ua)

        # WeChat
        if 'MicroMessenger' in ua:
            self.browser['name'] = 'WeChat'
            match = optimizedSearch(r'MicroMessenger\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # QQ Browser
        elif 'MQQBrowser' in ua or 'QQBrowser' in ua:
            self.browser['name'] = 'QQBrowser'
            match = optimizedSearch(r'(?:MQQBrowser|QQBrowser)\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # UC Browser
        elif 'UCBrowser' in ua:
            self.browser['name'] = 'UCBrowser'
            match = optimizedSearch(r'UCBrowser\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Sogou Browser
        elif 'SE' in ua and 'MetaSr' in ua or 'SogouMobileBrowser' in ua:
            self.browser['name'] = 'SogouBrowser'
            match = optimizedSearch(r'SogouMobileBrowser\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Baidu App
        elif 'baiduboxapp' in ua:
            self.browser['name'] = 'BaiduApp'
            match = optimizedSearch(r'baiduboxapp\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Baidu Browser
        elif 'BIDUBrowser' in ua or 'baidubrowser' in ua:
            self.browser['name'] = 'BaiduBrowser'
            match = optimizedSearch(r'(?:BIDUBrowser|baidubrowser)[\s\/]([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # 360 Browser
        elif '360SE' in ua or '360EE' in ua or 'QihooBrowser' in ua:
            self.browser['name'] = '360Browser'
            match = optimizedSearch(r'QihooBrowser\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Liebao Browser
        elif 'LBBROWSER' in ua or 'LieBaoFast' in ua:
            self.browser['name'] = 'LiebaoBrowser'
            self.browser['stock'] = False
            return True

        # 2345 Browser
        elif '2345Explorer' in ua or '2345Browser' in ua:
            self.browser['name'] = '2345Browser'
            match = optimizedSearch(r'2345(?:Explorer|Browser)\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Maxthon
        elif 'Maxthon' in ua or 'MXiOS' in ua:
            self.browser['name'] = 'Maxthon'
            match = optimizedSearch(r'(?:Maxthon|MXiOS)[\s\/]([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # MIUI Browser
        elif 'MiuiBrowser' in ua:
            self.browser['name'] = 'MIUIBrowser' # 'MIUI Browser'
            match = optimizedSearch(r'MiuiBrowser\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Samsung Browser
        elif 'SamsungBrowser' in ua:
            self.browser['name'] = 'SamsungBrowser'
            match = optimizedSearch(r'SamsungBrowser\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Huawei Browser
        elif 'HuaweiBrowser' in ua:
            self.browser['name'] = 'HuaweiBrowser'
            match = optimizedSearch(r'HuaweiBrowser\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # VIVO Browser
        elif 'VivoBrowser' in ua:
            self.browser['name'] = 'VIVOBrowser'
            match = optimizedSearch(r'VivoBrowser\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # OPPO Browser
        elif 'HeyTapBrowser' in ua or 'OppoBrowser' in ua:
            self.browser['name'] = 'OPPOBrowser'
            match = optimizedSearch(r'(?:HeyTapBrowser|OppoBrowser)\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Lenovo Browser
        elif 'SLBrowser' in ua or 'LeBrowser' in ua:
            self.browser['name'] = 'LenovoBrowser'
            match = optimizedSearch(r'(?:SLBrowser|LeBrowser)[\s\/]([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Chrome
        elif 'Chrome' in ua and 'Chromium' not in ua:
            self.browser['name'] = 'Chrome'
            match = optimizedSearch(r'Chrome\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Edge
        elif 'Edg' in ua:
            self.browser['name'] = 'Edge'
            match = optimizedSearch(r'Edg\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Firefox
        elif 'Firefox' in ua:
            self.browser['name'] = 'Firefox'
            match = optimizedSearch(r'Firefox\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Opera
        elif 'OPR' in ua or 'Opera' in ua:
            self.browser['name'] = 'Opera'
            match = optimizedSearch(r'(?:OPR|Opera)[\/]([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = False
            return True

        # Internet Explorer
        elif 'MSIE' in ua or 'Trident' in ua:
            self.browser['name'] = 'InternetExplorer'
            if 'MSIE' in ua:
                match = optimizedSearch(r'MSIE ([\d\.]+)', ua)
            else:
                match = optimizedSearch(r'rv:([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = True
            return True

        # Safari
        # 如果是Android设备，不识别为Safari
        elif 'Safari' in ua and 'Chrome' not in ua and 'Chromium' not in ua and 'Android' not in ua:
            self.browser['name'] = 'Safari'
            match = optimizedSearch(r'Version\/([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = True
            return True

        # Android Browser
        elif 'Android' in ua and 'Chrome' not in ua:
            self.browser['name'] = 'AndroidBrowser'
            match = optimizedSearch(r'Android[\s\/]([\d\.]+)', ua)
            if match:
                self.browser['version'] = Version({'value': match.group(1)})
            self.browser['stock'] = True
            return True

        return False