from version import Version
from utils import optimizedSearch, getMatch, cleanupModel

class DeviceDetector:
    """设备检测类"""
    def __init__(self):
        self.device = {
            'type': 'desktop',
            'identified': False,
            'manufacturer': '',
            'model': ''
        }

    def detect(self, ua):
        """检测设备品牌和型号"""
        if not ua:
            return False

        # 设置设备类型
        if 'Mobile' in ua or 'Android' in ua:
            self.device['type'] = 'mobile'
            if 'Mobile' not in ua and 'Android' in ua:
                self.device['type'] = 'tablet'

        # 如果不是移动设备或平板，直接返回
        if self.device['type'] not in ['mobile', 'tablet']:
            return False

        # Apple 设备
        if 'iPhone' in ua or 'iPad' in ua or 'iPod' in ua:
            self.device['manufacturer'] = 'Apple'
            if 'iPad' in ua:
                self.device['model'] = 'iPad'
            elif 'iPod' in ua:
                self.device['model'] = 'iPod'
            elif 'iPhone' in ua:
                self.device['model'] = 'iPhone'
            self.device['identified'] = True
            return True

        # Honor (需要在华为之前检测，因为有些老的UA中Honor和HUAWEI同时存在)
        elif 'HONOR' in ua or 'HonorBot' in ua or 'Build/HONOR' in ua:
            self.device['manufacturer'] = 'Honor'
            self.device['model'] = 'Honor'
            return True

        # Huawei (在Honor之后检测)
        # NX型号归属说明：
        # - NXT-AL10, NXT-TL00, NXT-CL00, NXT-DL00 等属于华为Mate 8
        # - NX619J, NX606J 等属于努比亚
        elif ('HUAWEI' in ua or 'HuaweiBrowser' in ua or 'Build/HUAWEI' in ua or
              optimizedSearch(r';\s*(?:NXT-[A-Z]{2}[0-9]{2}|SP[0-9]{3}|[A-Z]{3}-[A-Z]{2}[0-9]{2})\s+', ua) or
              'HMSCore' in ua):
            self.device['manufacturer'] = 'Huawei'
            self.device['model'] = ''

            # 首先尝试匹配三字母-两字母数字格式 (如 NOH-AN00)
            match = optimizedSearch(r';\s*([A-Z]{3}-[A-Z]{2}[0-9]{2})', ua)
            if match:
                self.device['model'] = match.group(1)
            # 然后尝试匹配Build信息中的型号
            elif optimizedSearch(r'(?:Build/HUAWEI)?([\w-]+)\s+Build/', ua):
                match = optimizedSearch(r'(?:Build/HUAWEI)?([\w-]+)\s+Build/', ua)
                self.device['model'] = match.group(1)
            # 如果没找到，再尝试之前的匹配方式
            elif optimizedSearch(r'HUAWEI[\s_-]([\w-]+)', ua):
                match = optimizedSearch(r'HUAWEI[\s_-]([\w-]+)', ua)
                self.device['model'] = match.group(1)
            # 如果还没找到，尝试匹配SP系列
            elif optimizedSearch(r';\s*(SP[0-9]{3})', ua):
                match = optimizedSearch(r';\s*(SP[0-9]{3})', ua)
                self.device['model'] = match.group(1)
            return True

        # Meizu (在小米之前检测，避免MZ开头型号被误判为小米)
        elif 'MZ-' in ua or 'MZBrowser' in ua or 'MEIZU' in ua:
            self.device['manufacturer'] = 'Meizu'
            self.device['model'] = ''

            # 匹配 MZ- 开头的型号
            match = optimizedSearch(r'MZ-([\w-]+)\s+Build\/', ua)
            if match:
                self.device['model'] = match.group(1)
            # 匹配其他可能的型号格式
            elif optimizedSearch(r'MEIZU[\s-]([\w-]+)', ua):
                match = optimizedSearch(r'MEIZU[\s-]([\w-]+)', ua)
                self.device['model'] = match.group(1)
            return True

        # Nubia (在华为之后检测)
        # NX型号说明：
        # - NX619J, NX606J, NX563J, NX513J 等属于努比亚
        # - 通常格式为 NX + 3位数字 + 字母
        elif 'nubia' in ua or optimizedSearch(r';\s*NX[0-9]{3}[A-Z]\s+Build\/', ua):
            self.device['manufacturer'] = 'Nubia'
            self.device['model'] = ''

            # 匹配 Build 前的型号
            match = optimizedSearch(r';\s*([\w-]+)\s+Build\/', ua)
            if match:
                self.device['model'] = match.group(1)
            # 匹配 nubia 后的型号
            elif optimizedSearch(r'nubia\s+([\w-]+)', ua):
                match = optimizedSearch(r'nubia\s+([\w-]+)', ua)
                self.device['model'] = match.group(1)
            return True

        # OPPO
        elif 'OPPO' in ua or 'OppoBrowser' in ua or 'HeyTapBrowser' in ua or optimizedSearch(r';\s*(?:OPPO|P[A-Z]{2})[A-Z0-9]+\s+Build\/', ua):
            self.device['manufacturer'] = 'OPPO'
            self.device['model'] = ''

            # 先尝试匹配Build前的型号 - 使用更通用的格式
            match = optimizedSearch(r';\s*((?:OPPO|P[A-Z]{2})[A-Z0-9]+)\s+Build\/', ua)
            if match:
                self.device['model'] = match.group(1)
            # 如果没找到，尝试其他可能的格式
            elif optimizedSearch(r';\s*OPPO\s*([A-Za-z][0-9]\w*)', ua):
                match = optimizedSearch(r';\s*OPPO\s*([A-Za-z][0-9]\w*)', ua)
                self.device['model'] = match.group(1)

            self.device['identified'] = True
            return True

        # vivo
        elif 'vivo' in ua.lower() or 'VivoBrowser' in ua or optimizedSearch(r';\s*V\d{4}[A-Z]{1,2}\b', ua):
            self.device['manufacturer'] = 'vivo'
            self.device['model'] = ''

            # 匹配vivo型号 (如 V2352A)
            match = optimizedSearch(r';\s*(V[0-9]{4}[A-Z]{1,2})\b', ua)
            if match:
                self.device['model'] = match.group(1)
            # 备用匹配模式
            elif optimizedSearch(r'vivo\s*([A-Za-z][0-9][A-Za-z0-9]+)', ua):
                match = optimizedSearch(r'vivo\s*([A-Za-z][0-9][A-Za-z0-9]+)', ua)
                self.device['model'] = match.group(1)

            self.device['identified'] = True
            return True

        # Samsung
        elif getMatch(ua, r'SAMSUNG|Galaxy|GT-|SM-|SCH-|SGH-', True):
            match = getMatch()
            self.device['manufacturer'] = 'Samsung'
            if getMatch(ua, r';\s*(Galaxy [^/;]*|GT-[a-zA-Z0-9]+|SM-[a-zA-Z0-9]+|SCH-[a-zA-Z0-9]+|SGH-[a-zA-Z0-9]+)\s+Build\/', True):
                match = getMatch()
                self.device['model'] = match.group(1)
            self.device['identified'] = True
            return True

        # OnePlus
        elif getMatch(ua, r'OnePlus|ONEPLUS', True):
            match = getMatch()
            self.device['manufacturer'] = 'OnePlus'
            if getMatch(ua, r'ONEPLUS[ _]([a-zA-Z0-9]+)', True):
                match = getMatch()
                self.device['model'] = match.group(1)
            self.device['identified'] = True
            return True

        # Realme
        if getMatch(ua, r'Realme|RMX[0-9]+', True):
            match = getMatch()
            self.device['manufacturer'] = 'Realme'
            if getMatch(ua, r'(RMX[0-9]+)', True):
                match = getMatch()
                self.device['model'] = match.group(1)
            self.device['identified'] = True
            return True

        # Xiaomi & Redmi
        if getMatch(ua, r'(Xiaomi|Redmi|MI|HM|MIX|Mi9|Mi 9|Mi10|Mi 10|M2|M3|M4|M5|M6|M7|M8)', True):
            match = getMatch()
            self.device['manufacturer'] = 'Xiaomi'
            if match.group(1).startswith('Redmi'):
                self.device['model'] = match.group(1)
            elif match.group(1).startswith(('MI', 'Mi')):
                self.device['model'] = match.group(1)
            self.device['identified'] = True
            return True

        # 金立
        elif 'GIONEE' in ua or 'GN' in ua or optimizedSearch(r';\s*F[\d]{3}\s+Build\/', ua):
            self.device['manufacturer'] = 'Gionee'
            self.device['model'] = ''

            # 匹配 Build 前的型号 (F103, M7等)
            match = optimizedSearch(r';\s*((?:F|M|S|GN)[\w-]+)\s+Build\/', ua)
            if match:
                self.device['model'] = match.group(1)
            # 匹配 GIONEE 后的型号
            elif optimizedSearch(r'GIONEE[\s-]([\w-]+)', ua):
                match = optimizedSearch(r'GIONEE[\s-]([\w-]+)', ua)
                self.device['model'] = match.group(1)
            return True

        # Google (需要在其他Android设备之前检测)
        elif 'Pixel' in ua or 'Google' in ua or optimizedSearch(r';\s*(?:Pixel|Nexus)\s+\d', ua):
            self.device['manufacturer'] = 'Google'
            self.device['model'] = ''

            # Pixel 系列
            match = optimizedSearch(r'Pixel\s+(?:\d[a-zA-Z]?|XL|Fold|[a-zA-Z]+)(?:\s+5G)?', ua)
            if match:
                self.device['model'] = match.group(0)
                return True

            # Nexus 系列 (Google 品牌的 Nexus)
            match = optimizedSearch(r'Nexus\s+(One|[4-9]|6P|5X|Player|10)(?:\s+Build|[;\)])', ua)
            if match:
                self.device['model'] = 'Nexus ' + match.group(1)
                return True

            # 其他 Google 设备
            match = optimizedSearch(r'Google\s+([^;\/\)]+)', ua)
            if match:
                self.device['model'] = match.group(1).strip()
                return True

            return True

        # Xiaomi
        elif 'XiaoMi' in ua or 'MI ' in ua or 'MiuiBrowser' in ua or 'MIUI' in ua or optimizedSearch(r';\s*(?:MI|Mi|Redmi|HM|2[0-9])[A-Z0-9]+', ua):
            self.device['manufacturer'] = 'Xiaomi'
            self.device['model'] = ''

            # 匹配数字型号 (如 2211133C)
            match = optimizedSearch(r';\s*(2[0-9][0-9][0-9][0-9][0-9][0-9][0-9][A-Z0-9]+)\s+Build', ua)
            if match:
                self.device['model'] = match.group(1)
            # 匹配传统型号
            elif optimizedSearch(r';\s*(?:MI|Mi|Redmi|HM)[ -]([A-Za-z0-9 ]+)\s+Build', ua):
                match = optimizedSearch(r';\s*(?:MI|Mi|Redmi|HM)[ -]([A-Za-z0-9 ]+)\s+Build', ua)
                self.device['model'] = match.group(1).strip()

            self.device['identified'] = True
            return True

        # 其他品牌的通用检测
        other_brands = [
            ('Motorola', r'Motorola|Moto[ _]([a-zA-Z0-9]+)'),
            ('LG', r'LG[ _-]([a-zA-Z0-9]+)'),
            ('Sony', r'Sony([a-zA-Z0-9]+)'),
            ('HTC', r'HTC[ _-]([a-zA-Z0-9]+)'),
            ('Nokia', r'Nokia[ _]([a-zA-Z0-9\-]+)'),
            ('Lenovo', r'Lenovo[ _-]([a-zA-Z0-9]+)'),
            ('ZTE', r'ZTE[ _]([a-zA-Z0-9\-]+)'),
            ('TCL', r'TCL[ _]([a-zA-Z0-9]+)'),
            ('Coolpad', r'Coolpad[ _]([a-zA-Z0-9]+)'),
            ('ASUS', r'ASUS[ _]([a-zA-Z0-9]+)'),
            ('BlackBerry', r'BlackBerry[ _]([a-zA-Z0-9]+)')
        ]

        for brand, pattern in other_brands:
            if getMatch(ua, pattern, True):
                match = getMatch()
                self.device['manufacturer'] = brand
                if match.group(1):
                    self.device['model'] = match.group(1)
                self.device['identified'] = True
                return True

        # 清理设备型号
        if self.device['model']:
            self.device['model'] = cleanupModel(self.device['model'])

        return self.device['identified']