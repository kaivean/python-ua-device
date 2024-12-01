# 操作系统版本映射
WINDOWS_VERSIONS = {
    '10.0.2': '11',
    '10.0': '10',
    '6.3': '8.1',
    '6.2': '8',
    '6.1': '7',
    '6.0': 'Vista',
    '5.2': 'Server 2003/XP x64',
    '5.1': 'XP',
    '5.0': '2000'
}

# 浏览器正则表达式
BROWSER_REGEX = {
    'WeChat': r'MicroMessenger\/([\d\.]+)',
    'QQ': r'(?:MQQBrowser|QQBrowser)\/([\d\.]+)',
    'UC': r'UCBrowser\/([\d\.]+)',
    'Sogou': r'SogouMobileBrowser\/([\d\.]+)',
    'Baidu': r'(?:BIDUBrowser|baidubrowser)[\s\/]([\d\.]+)',
    '360': r'QihooBrowser\/([\d\.]+)',
    '2345': r'2345(?:Explorer|Browser)\/([\d\.]+)',
    'Maxthon': r'(?:Maxthon|MXiOS)[\s\/]([\d\.]+)',
    'MIUI': r'MiuiBrowser\/([\d\.]+)',
    'Samsung': r'SamsungBrowser\/([\d\.]+)',
    'Huawei': r'HuaweiBrowser\/([\d\.]+)',
    'VIVO': r'VivoBrowser\/([\d\.]+)',
    'OPPO': r'HeyTapBrowser\/([\d\.]+)',
    'Chrome': r'Chrome\/([\d\.]+)',
    'Edge': r'Edg\/([\d\.]+)',
    'Firefox': r'Firefox\/([\d\.]+)',
    'Opera': r'(?:OPR|Opera)[\/]([\d\.]+)',
    'IE': r'MSIE ([\d\.]+)|rv:([\d\.]+)',
    'Safari': r'Version\/([\d\.]+)',
    'Android': r'Android[\s\/]([\d\.]+)'
}

# 设备品牌正则表达式
DEVICE_REGEX = {
    'Huawei': r'(Huawei[\s\-_](\w*[-_]?\w*)|\s(7D-\w*|ALE-\w*|ATH-\w*|CHE-\w*|CHM-\w*|Che1-\w*|Che2-\w*|D2-\w*|G616-\w*|G620S-\w*|G621-\w*|G660-\w*|G750-\w*|GRA-\w*|Hol-\w*|MT2-\w*|MT7-\w*|PE-\w*|PLK-\w*|SC-\w*|SCL-\w*|H60-\w*|H30-\w*)[\s\)])',
    'Honor': r'(Build/HONOR|HW-CHM|HONOR)',
    'Xiaomi': r';\s(mi|m[1-9]|redmi)(\s+\w*)[\s\)]',
    'OPPO': r'OPPO[ _]?([a-zA-Z0-9]+)',
    'vivo': r'vivo[ _]([a-zA-Z0-9]+)',
    'Samsung': r'[-\s](Galaxy[\s\-_]nexus|Galaxy[\s\-_]\w*[\s\-_]\w*|Galaxy[\s\-_]\w*|SM-\w*|GT-\w*|s[cgp]h-\w*|shw-\w*)',
    'Realme': r'Realme[ _]([a-zA-Z0-9]+)',
    'OnePlus': r'ONEPLUS[ _]([a-zA-Z0-9]+)',
    'Meizu': r'(M[0-9]+[a-zA-Z]?|MZ-[a-zA-Z0-9]+)',
    'ZTE': r'ZTE[ _-]([a-zA-Z0-9\-]+)',
    'Lenovo': r'Lenovo[ _-]([a-zA-Z0-9]+)',
    'Motorola': r'Motorola|Moto[ _-]([a-zA-Z0-9]+)',
    'Nokia': r'Nokia[ _]([a-zA-Z0-9\-]+)',
    'Sony': r'Sony([a-zA-Z0-9]+)|([a-zA-Z0-9]+)Sony',
    'LG': r'LG[ _-]([a-zA-Z0-9]+)',
    'TCL': r'TCL[ _]([a-zA-Z0-9]+)',
    'Coolpad': r'Coolpad[ _]([a-zA-Z0-9]+)',
    'ASUS': r'ASUS[ _]([a-zA-Z0-9]+)',
    'BlackBerry': r'BlackBerry[ _]([a-zA-Z0-9]+)',
    'Google': r'Pixel[ _]([a-zA-Z0-9]+)'
}

# 操作系统正则表达式
OS_REGEX = {
    'HarmonyOS': r'OpenHarmony\s?([0-9.]+)',
    'iOS': r'OS ([\d_]+) like Mac OS X',
    'Android': r'Android[\s\/]+([\d\.]+)',
    'Windows': r'Windows NT ([\d\.]+)',
    'Mac': r'Mac OS X ([\d_\.]+)',
    'Ubuntu': r'Ubuntu[\/\s]([\d\.]+)',
    'CentOS': r'CentOS[\/\s]+([\d\.]+)',
    'Debian': r'Debian[\/\s]+([\d\.]+)',
    'RedHat': r'Red Hat[\/\s]+([\d\.]+)',
    'Fedora': r'Fedora[\/\s]+([\d\.]+)'
}